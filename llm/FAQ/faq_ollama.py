import sys
import json
from pathlib import Path
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from logging_util.logger import get_logger

logger = get_logger()
chunks_path = project_root / "chunking" / "chunks.json"


def load_knowledge_base(filepath=chunks_path, max_chunks=25):
    """
    Carga el archivo con los chunks del conocimiento y selecciona los más relevantes
    para evitar exceder el límite de contexto del modelo.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    selected = sorted(data, key=lambda x: len(x["content"]), reverse=True)[:max_chunks]
    context = "\n".join([item["content"] for item in selected])

    logger.info(f"✅ Base de conocimiento cargada. {len(selected)} fragmentos seleccionados de {len(data)} totales.")
    logger.info(f"📏 Tamaño aproximado del contexto: {len(context.split())} palabras.\n")
    return context


def create_faq_chain(llm_model="gpt-oss:20b"):
    """
    Crea una cadena LangChain que genera automáticamente preguntas frecuentes (FAQ)
    sobre Colombina, basadas en la base de conocimiento.
    """
    llm = Ollama(model=llm_model)

    template = """
    Eres un generador de Preguntas Frecuentes (FAQ) sobre la empresa **Colombina**, 
    un líder latinoamericano en alimentos. Tu tarea es analizar la base de conocimiento 
    provista y producir directamente entre 15 y 25 preguntas realistas y diversas 
    que un cliente, proveedor o colaborador podría hacer sobre la empresa.

    Reglas:
    - Las preguntas deben centrarse en Colombina: su historia, productos, sostenibilidad, 
      innovación, programas sociales, proveedores y contacto.
    - No generes preguntas genéricas sobre liderazgo o gestión.
    - No pidas aclaraciones al usuario ni solicites más información.
    - No incluyas respuestas ni formato adicional, solo las preguntas enumeradas.
    - Redacta las preguntas en tono formal y natural, como en una sección de FAQ corporativa.

    --- INICIO DE LA BASE DE CONOCIMIENTO ---
    {context}
    --- FIN DE LA BASE DE CONOCIMIENTO ---

    Preguntas frecuentes:
    """

    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    return chain


def main():
    context = load_knowledge_base()

    faq_chain = create_faq_chain(llm_model="gpt-oss:20b")

    logger.info("\n--- 🚀 GENERANDO PREGUNTAS FRECUENTES DE COLOMBINA ---\n")

    faqs = faq_chain.invoke({"context": context})
    logger.info(faqs)

    output_file = project_root / "llm" / "FAQ" / "faqs_colombina.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(faqs)

    logger.info(f"\n✅ Preguntas frecuentes guardadas en '{output_file}'.")


if __name__ == "__main__":
    main()