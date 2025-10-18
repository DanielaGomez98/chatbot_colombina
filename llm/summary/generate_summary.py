import json
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def load_knowledge_base(filepath="chunks.json"):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    context = "\n".join([item["content"] for item in data])
    print(f"✅ Base de conocimiento cargada. {len(data)} fragmentos.")
    return context


def create_summary_chain(knowledge_context, llm_model="gpt-oss:20b"):
    llm = Ollama(model=llm_model)

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


def main():
    context = load_knowledge_base()
    summary_chain = create_summary_chain(context, llm_model="gpt-oss:20b")

    print("\n--- 🚀 GENERANDO RESUMEN GLOBAL ---\n")
    summary = summary_chain.invoke({"context": context})
    print(summary)

if __name__ == "__main__":
    main()