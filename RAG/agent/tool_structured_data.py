import os
import sys
import json
from pathlib import Path
from langchain_core.tools import tool

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from logging_util.logger import get_logger

logger = get_logger()

company_data_file = "company_data.json"
company_data_path = project_root / "RAG" / "agent" / company_data_file


def load_structured_data() -> dict:
    """
    Carga los datos desde el archivo JSON.
    Si el archivo no existe, crea uno de ejemplo.
    """
    try:
        if not company_data_path.exists():
            logger.warning(f"⚠️ Archivo '{company_data_file}' no encontrado, creando datos de ejemplo")
            example_data = {
                "contacto": {
                    "telefono_servicio_cliente": "+57 1 234 5678",
                    "email_soporte": "soporte@colombina.com"
                },
                "horarios": {
                    "atencion_telefonia_lu_vi": "8:00 AM - 5:00 PM",
                    "atencion_telefonia_sa": "9:00 AM - 12:00 PM",
                    "chat_online": "24/7"
                },
                "sedes_cali": ["Sede Norte - Av. 6N #20-10", "Sede Sur - Calle 5 #66-15"],
                "nit": "890.301.234-5"
            }
            with open(company_data_path, 'w', encoding='utf-8') as f:
                json.dump(example_data, f, indent=4, ensure_ascii=False)
            return example_data
        
        with open(company_data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    except Exception as e:
        logger.error(f"❌ Error crítico cargando '{company_data_file}': {e}")
        return {"error": f"No se pudieron cargar los datos estructurados. {e}"}


@tool
def search_structured_data(pregunta_clave: str) -> str:
    """
    Usa esta herramienta SÓLO para preguntas MUY específicas sobre datos concretos como:
    'telefono', 'horario', 'email', 'nit' o 'sedes en Cali'.
    La 'pregunta_clave' debe ser simple y describir el dato buscado.
    Ejemplos de pregunta_clave: 'telefono_servicio_cliente', 'horarios_atencion', 'nit', 'sedes_cali'.
    """
    logger.info(f"🔍 Buscando datos estructurados con clave: '{pregunta_clave}'")
    
    data = load_structured_data()
    
    if "error" in data:
        return json.dumps(data)

    search_key = pregunta_clave.lower().strip().replace(" ", "_")
    
    if "telefono" in search_key or "servicio" in search_key or "contacto" in search_key:
        result = data.get("contacto", {"info": "Dato de contacto no encontrado."})
    elif "horario" in search_key or "atencion" in search_key:
        result = data.get("horarios", {"info": "Dato de horarios no encontrado."})
    elif "sedes" in search_key and "cali" in search_key:
        result = {"sedes_cali": data.get("sedes_cali", [])}
    elif "nit" in search_key:
        result = {"nit": data.get("nit", "NIT no encontrado.")}
    else:
        result = {"error": "No se encontraron datos para esa clave específica."}

    return json.dumps(result, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    logger.info("🧪 Iniciando pruebas de datos estructurados")
    
    logger.info("📂 Verificando y cargando archivo de datos...")
    load_structured_data()
    
    logger.info("📝 Prueba 1: Consulta de teléfono")
    response1 = search_structured_data.invoke({"pregunta_clave": "telefono_servicio_cliente"})
    logger.info(f"📋 Respuesta JSON: {response1}")

    logger.info("📝 Prueba 2: Consulta de horarios")
    response2 = search_structured_data.invoke({"pregunta_clave": "horarios_atencion"})
    logger.info(f"📋 Respuesta JSON: {response2}")

    logger.info("📝 Prueba 3: Consulta de NIT")
    response3 = search_structured_data.invoke({"pregunta_clave": "nit"})
    logger.info(f"📋 Respuesta JSON: {response3}")

    logger.info("📝 Prueba 4: Consulta fallida (información no disponible)")
    response4 = search_structured_data.invoke({"pregunta_clave": "mision_de_la_empresa"})
    logger.info(f"📋 Respuesta JSON: {response4}")