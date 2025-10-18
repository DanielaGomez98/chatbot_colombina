import os
import sys
import json
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from logging_util.logger import get_logger
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
chunks_path = project_root / "chunking" / "chunks.json"

logger = get_logger()


def load_knowledge_base(filepath=chunks_path):
    """
    Carga los chunks desde el archivo JSON y los concatena en un solo
    string de texto que servirá como contexto completo.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        full_context = ""
        for item in data:
            title = item['metadata'].get('title', 'Fuente desconocida')
            source_file = item['metadata'].get('source_file', 'Documento sin nombre')
            
            full_context += f"--- Inicio del Documento: {title} (Archivo: {source_file}) ---\n"
            full_context += item['content']
            full_context += f"\n--- Fin del Documento: {title} ---\n\n"
            
        logger.info(f"✅ Base de conocimiento cargada y consolidada. Total de caracteres: {len(full_context)}")
        return full_context
    except FileNotFoundError:
        logger.error(f"❌ Error: El archivo '{filepath}' no fue encontrado.")
        return None
    except Exception as e:
        logger.error(f"❌ Ocurrió un error al cargar la base de conocimiento: {e}")
        return None


def create_simple_qa_chain(llm_model="gpt-4o"):
    """
    Crea una cadena de Q&A simple usando OpenAI.
    """
    logger.info(f"\n🔄 Configurando la cadena Q&A con OpenAI: '{llm_model}'...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("❌ Falta la API Key de OpenAI")
        return None

    llm = ChatOpenAI(
        model=llm_model,
        temperature=0.1,
        top_p=0.9,
        api_key=api_key,
        max_tokens=1024
    )

    template = """
    Eres un asistente experto de la empresa Colombina. Responde la pregunta del usuario basándote estricta y únicamente en la siguiente base de conocimiento.
    Si la respuesta no se encuentra en la base de conocimiento, responde exactamente: "La información solicitada no se encuentra en mi base de conocimiento."
    No intentes inventar una respuesta. Sé conciso y directo.

    --- INICIO DE LA BASE DE CONOCIMIENTO ---
    {context}
    --- FIN DE LA BASE DE CONOCIMIENTO ---

    Pregunta del usuario:
    {question}

    Respuesta:
    """
    prompt = PromptTemplate.from_template(template)

    simple_qa_chain = (
        prompt
        | llm
        | StrOutputParser()
    )
    
    logger.info("✅ Cadena de Q&A simple configurada exitosamente.")
    return simple_qa_chain

def main():
    knowledge_context = load_knowledge_base()
    if knowledge_context is None:
        return

    qa_chain = create_simple_qa_chain(llm_model="gpt-4o")
    if qa_chain is None:
        return

    questions = [
        "¿En qué año se creó el Bon Bon Bum?",
        "¿Cómo se llama el programa de Colombina para acompañar a sus proveedores y emprendedores?",
        "¿Qué porcentaje de la energía eléctrica que utiliza Colombina en sus operaciones en Colombia proviene de fuentes renovables?",
        "¿Cuál es la certificación que han recibido las 5 fábricas de Colombia en relación con la gestión de residuos?",
        "¿Quién fue el fundador de Colombina?",
        "Describe la colaboración entre Bon Bon Bum y Tajín. ¿Qué producto lanzaron y cuáles eran las proyecciones de ventas?",
        "¿Cuáles son los principales logros de Colombina en materia de sostenibilidad relacionados con la energía y el agua?",
        "Según la política de protección de datos, ¿cuál es el procedimiento que debe seguir una persona si desea actualizar o rectificar su información personal?",
        "Resume la historia de la creación de la chupeta Bon Bon Bum. ¿Quién la creó y cuál fue su innovación principal?",
        "¿Qué es Colombina Energía S.A.S. E.S.P. y cuál es su función principal?",
        "Compara las alianzas de Colombina con Ramo y Postobón. ¿Qué productos icónicos se crearon en cada colaboración?",
        "¿Qué relación existe entre la certificación 'Sello Oro Equipares' y los valores corporativos de Colombina?",
        "Lista tres plantas de producción de Colombina, su ubicación y qué tipo de productos se fabrican en cada una.",
        "¿En qué países fuera de Colombia tiene Colombina plantas de producción, según la información proporcionada?",
        "Si soy un proveedor y no he logrado obtener mi certificado de retención a través del portal, ¿a qué correo electrónico debo escribir?",
        "¿Cuál es la política de Colombina respecto al uso de huevos libres de jaula y cuál es la meta para 2025?",
        "De acuerdo con la política de tratamiento de datos, ¿qué ocurre con la información de un candidato que no es seleccionado para un puesto de trabajo?",
        "¿Cuál fue la calificación que recibió Colombina al obtener la certificación Basura Cero ORO para sus plantas de helados?",
        "Menciona dos deportistas que han sido embajadores o imagen de campañas relacionadas con Bon Bon Bum.",
        "¿Cuál es el salario anual del presidente de Colombina?"
    ]

    logger.info("\n--- 🚀 INICIANDO EVALUACIÓN DEL SISTEMA Q&A (MÉTODO IN-CONTEXT) 🚀 ---\n")
    
    for i, question in enumerate(questions, 1):
        logger.info(f"--- Pregunta {i}/{len(questions)} ---")
        logger.info(f"❓: {question}")
        
        answer = qa_chain.invoke({"context": knowledge_context, "question": question})
        
        logger.info(f"🤖: {answer}")
        logger.info("-" * (len(str(i)) + len(str(len(questions))) + 16))
        logger.info("\n")

if __name__ == "__main__":
    main()



# def procesar_pregunta_colombina(pregunta: str, temperatura: float = 0.5, top_p: float = 0.9):
#     """
#     Procesa la pregunta del usuario usando el modelo OpenAI con parámetros configurables.
    
#     Args:
#         pregunta (str): La pregunta del usuario
#         temperatura (float): Controla la creatividad (0.0 - 1.0)
#         top_p (float): Controla la diversidad (0.0 - 1.0)
    
#     Returns:
#         str: Respuesta del modelo
#     """
#     try:
#         api_key = os.getenv("OPENAI_API_KEY")
#         if not api_key:
#             return """⚠️ **Falta la API Key de OpenAI**
            
# Para configurar tu API Key:
# 1. Obtén tu API Key en: https://platform.openai.com/api-keys
# 2. Crea un archivo `.env` en la carpeta del proyecto
# 3. Agrega: `OPENAI_API_KEY=tu_api_key_aqui`
# 4. O ejecuta: `export OPENAI_API_KEY=tu_api_key_aqui`"""
        
#         llm = ChatOpenAI(
#             model="gpt-4o",
#             temperature=temperatura,
#             top_p=top_p,
#             api_key=api_key
#         )
        
#         template = """Eres un asistente virtual especializado en la empresa Colombina, líder en dulces y confitería en Colombia y Latinoamérica. 
        
# Responde de manera amigable, profesional y con conocimiento sobre:
# - Productos Colombina (dulces, chocolates, confitería)
# - Historia y valores de la empresa
# - Disponibilidad de productos
# - Ingredientes y información nutricional
# - Promociones y novedades

# Pregunta: {question}
# Respuesta:"""
        
#         prompt = PromptTemplate.from_template(template)
        
#         chain = prompt | llm
        
#         respuesta = chain.invoke({"question": pregunta})
        
#         return respuesta.content.strip()
        
#     except Exception as e:
#         return f"⚠️ Error al procesar la pregunta: {str(e)}"