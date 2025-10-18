import sys
import json
from pathlib import Path
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from logging_util.logger import get_logger

logger = get_logger()
chunks_path = project_root / "chunking" / "chunks.json"


def load_knowledge_base(filepath=chunks_path):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    context = "\n".join([item["content"] for item in data])
    logger.info(f"✅ Base de conocimiento cargada. {len(data)} fragmentos.")
    return context


def create_summary_chain(llm_model, temperature, top_p):
    llm = OllamaLLM(model=llm_model, temperature=temperature, top_p=top_p)

    template = """
    Eres un asistente experto en redacción y análisis empresarial.
    Genera un resumen claro, preciso y estructurado de la siguiente base de conocimiento de Colombina.
    No inventes información, y divide el resumen en secciones temáticas relevantes.

    --- INICIO DE LA BASE DE CONOCIMIENTO ---
    {context}
    --- FIN DE LA BASE DE CONOCIMIENTO ---

    Resumen:
    """

    prompt = PromptTemplate.from_template(template)

    chain = prompt | llm | StrOutputParser()
    return chain


def generate_summary(llm_model, temperature, top_p):
    context = load_knowledge_base()
    summary_chain = create_summary_chain(llm_model, temperature, top_p)
    summary = summary_chain.invoke({"context": context})

    return summary


def main(temperature=0.1, top_p=0.9):
    context = load_knowledge_base()
    summary_chain = create_summary_chain(llm_model="gpt-oss:20b", temperature=temperature, top_p=top_p)

    logger.info("\n--- 🚀 GENERANDO RESUMEN GLOBAL ---\n")
    summary = summary_chain.invoke({"context": context})
    logger.info(summary)

if __name__ == "__main__":
    main()