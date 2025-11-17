import re
from pathlib import Path
from collections import defaultdict

project_root = Path(__file__).parent.parent.parent
INPUT_FILE = project_root / "utils" / "knowledge_base" / "knowledge_base.txt"
OUTPUT_FILE = project_root / "utils" / "knowledge_base" / "improved_knowledge_base.txt"


SECCIONES = {
    "HISTORIA Y EXPANSIÓN": [
        "historia", "fundación", "origen", "trayectoria", "expansión", "crecimiento",
        "años", "internacionalización", "empresa familiar", "bon bon bum", "fundador"
    ],
    "SOSTENIBILIDAD": [
        "sostenibilidad", "ambiental", "carbono", "energía", "renovable", "agua", "basura cero",
        "reciclaje", "huella", "circular", "ODS", "medio ambiente", "paneles solares"
    ],
    "INNOVACIÓN Y NUTRICIÓN": [
        "innovación", "nutrición", "saludable", "clean", "clear", "investigación",
        "desarrollo", "tecnología", "productos saludables"
    ],
    "PRODUCTOS": [
        "producto", "marca", "portafolio", "línea", "alimentos", "confitería",
        "bebidas", "snacks", "chocolates", "galletas"
    ],
    "ECONOMÍA Y DESEMPEÑO": [
        "ventas", "utilidad", "ingreso", "financiero", "crecimiento económico", "rentabilidad",
        "ebitda", "balance", "resultados"
    ],
    "RESPONSABILIDAD SOCIAL": [
        "responsabilidad social", "comunidad", "fundación", "equidad", "inclusión",
        "equipares", "educación", "donación", "empleados", "diversidad", "voluntariado"
    ],
    "PROYECTOS DESTACADOS": [
        "proyecto", "iniciativa", "programa", "alianza", "colaboración", "premio",
        "innovador", "reconocimiento", "estrategia", "campaña"
    ],
    "CONTACTO": [
        "contacto", "correo", "email", "teléfono", "sede", "dirección", "servicio al cliente",
        "proveedores", "portal", "certificado", "reclamos"
    ]
}


def detectar_tema(texto):
    """Detecta la sección temática más probable para un fragmento."""
    texto_limpio = texto.lower()
    puntuaciones = {seccion: 0 for seccion in SECCIONES}
    for seccion, palabras in SECCIONES.items():
        puntuaciones[seccion] = sum(pal in texto_limpio for pal in palabras)

    return max(puntuaciones, key=puntuaciones.get)


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        contenido = f.read()

    documentos = re.split(r"(?m)^=== .* ===$", contenido)
    documentos = [doc.strip() for doc in documentos if doc.strip()]
    nombres = re.findall(r"(?m)^=== (.*) ===$", contenido)

    agrupado = defaultdict(list)

    for i, doc in enumerate(documentos):
        fuente = nombres[i] if i < len(nombres) else "Documento desconocido"
        tema = detectar_tema(doc)
        agrupado[tema].append(f"[Fuente: {fuente}]\n{doc.strip()}\n")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for seccion in SECCIONES.keys():
            f.write(f"=== {seccion} ===\n")
            if agrupado[seccion]:
                for bloque in agrupado[seccion]:
                    f.write(bloque + "\n")
            else:
                f.write("(Sin información relevante encontrada)\n\n")

    print(f"✅ Base de conocimiento reorganizada guardada en: {OUTPUT_FILE}")
    print("Secciones generadas:")
    for s, bloques in agrupado.items():
        print(f" - {s}: {len(bloques)} fragmentos")


if __name__ == "__main__":
    main()