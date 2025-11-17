import os
import sys
import json
from typing import List
from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, get_buffer_string

load_dotenv()

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.logging_util.logger import get_logger

logger = get_logger()

db_directory = project_root / "RAG" / "chroma_db"

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    logger.error("❌ API Key de OpenAI no encontrada en variables de entorno")
    raise ValueError("OPENAI_API_KEY no configurada")


try:  
    logger.info(f"🔍 Cargando base de datos vectorial desde: {db_directory}")
    vectorstore = Chroma(
        persist_directory=str(db_directory),
        embedding_function=OpenAIEmbeddings(api_key=API_KEY)
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    logger.info("✅ Base de datos vectorial cargada exitosamente")

except Exception as e:
    logger.error(f"❌ Error al cargar la base de datos de Chroma: {e}")
    retriever = None


llm = ChatOpenAI(model="gpt-4o", api_key=API_KEY, temperature=0)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", """Dada la siguiente conversación y la última pregunta, 
      reformula la pregunta para que sea una pregunta independiente que pueda ser entendida 
      sin el historial del chat. NO respondas la pregunta, solo reformúlala."""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])


def get_contextualized_question(input_data: dict):
    """Obtiene el historial y decide si reformular la pregunta."""
    history_str = get_buffer_string(input_data["history"])
    if history_str:
        contextualizer_chain = contextualize_q_prompt | llm
        return contextualizer_chain.invoke({
            "input": input_data["input"], 
            "history": input_data["history"]
        }).content
    return input_data["input"]


def retrieve_documents(input_data: dict):
    """Obtiene la pregunta (contextualizada o no) y busca en el retriever."""
    contextualized_question = input_data["contextualized_question"]
    if not retriever:
        logger.warning("⚠️ Retriever no inicializado, devolviendo 0 documentos")
        return []
    return retriever.invoke(contextualized_question)


qa_system_prompt = """Eres un asistente virtual especializado en la empresa Colombina. 
Usa ÚNICA Y ESTRICTAMENTE los siguientes documentos (contexto: {context}) para responder la pregunta del usuario.

Si la información no se encuentra en el contexto, responde exactamente: 
'La información solicitada no se encuentra en mi base de conocimiento.'

Sé amigable y profesional.

Pregunta del usuario: {question}
"""
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", qa_system_prompt),
])


def format_docs(docs):
    return "\n\n".join(
        doc.page_content.encode('utf-8', 'ignore').decode('utf-8') 
        for doc in docs
    )
    
rag_chain = RunnablePassthrough.assign(
    history=RunnableLambda(lambda x: x["history"]),
    contextualized_question=get_contextualized_question
).assign(
    context_docs=retrieve_documents
).assign(
    context=lambda x: format_docs(x["context_docs"])
).assign(
    question=lambda x: x["input"]
) | qa_prompt | llm


@tool
def consult_knowledge_base(question: str, conversation_history: List[dict]) -> str:
    """
    Usa esta herramienta para responder preguntas abiertas sobre la empresa, 
    sus productos, historia, valores, políticas, etc. 
    Esta herramienta consulta una base de conocimiento documental (RAG).
    """
    logger.info(f"� Consultando RAG con pregunta: '{question}'")
    
    history_messages = []
    for msg in conversation_history:
        if msg['type'] == 'human':
            history_messages.append(HumanMessage(content=msg['content']))
        elif msg['type'] == 'ai':
            history_messages.append(AIMessage(content=msg['content']))
    
    history_for_context = history_messages[:-1] if len(history_messages) > 0 else []

    try:
        response = rag_chain.invoke({
            "input": question,
            "history": history_for_context
        })
        text_response = response.content.strip()

        if text_response == "La información solicitada no se encuentra en mi base de conocimiento.":
            logger.info("� RAG no encontró información relevante")
            return json.dumps({"error": "La información solicitada no se encuentra en mi base de conocimiento."})

        logger.info("✅ RAG respondió exitosamente")
        return text_response
        
    except Exception as e:
        logger.error(f"❌ Error en consulta RAG: {e}")
        return json.dumps({"error": f"Error en la herramienta RAG: {e}"})


if __name__ == "__main__":
    logger.info("🧪 Iniciando pruebas de la herramienta RAG...")
    
    example_history = [
        {'type': 'human', 'content': 'Hola'},
        {'type': 'ai', 'content': 'Hola, ¿en qué puedo ayudarte?'}
    ]

    logger.info("📝 Prueba 1: Pregunta sobre información existente")
    rag_response = consult_knowledge_base.invoke({
        "question": "¿Quién fue el fundador de Colombina?", 
        "conversation_history": example_history
    })
    logger.info(f"📋 Respuesta: {rag_response}")

    logger.info("📝 Prueba 2: Pregunta sobre información inexistente")
    failed_response = consult_knowledge_base.invoke({
        "question": "¿Cuál es la receta de la Coca-Cola?", 
        "conversation_history": example_history
    })
    logger.info(f"📋 Respuesta: {failed_response}")