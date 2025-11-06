import os
import sys
import uuid
import json
import operator
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
from langgraph.checkpoint.memory import MemorySaver
from RAG.agent.tool_rag import consult_knowledge_base
from RAG.agent.tool_structured_data import search_structured_data
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage, BaseMessage


load_dotenv()

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from logging_util.logger import get_logger

logger = get_logger()

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    logger.error("❌ API Key de OpenAI no encontrada en variables de entorno")
    raise ValueError("OPENAI_API_KEY no configurada")


tools = [consult_knowledge_base, search_structured_data]
tool_node = ToolNode(tools)


class AgentState(TypedDict):
    """
    Define el estado del grafo.
    'messages' se acumulará con 'operator.add'.
    El estado persistirá diccionarios serializables (JSON).
    """
    messages: Annotated[List[dict], operator.add]


AGENT_SYSTEM_PROMPT = """Eres un agente conversacional asistente de Colombina.
Tu objetivo es responder a la pregunta del usuario de la mejor manera posible.
Analiza la conversación y la pregunta actual para decidir la mejor acción.

Tienes acceso a dos herramientas:

1.  `consult_knowledge_base`:
    Úsala para preguntas abiertas, complejas o que requieran contexto sobre la empresa, su **historia, valores, informes de sostenibilidad, o preguntas de opinión** que NO se encuentren en la lista de datos fácticos de la otra herramienta.
    Ej: "¿Cuál es la misión de Colombina?", "¿Por qué es importante la sostenibilidad para la empresa?"

2.  `search_structured_data`:
    Úsala SÓLO para preguntas que pidan datos MUY específicos y fácticos.
    Esta herramienta contiene información sobre:
    - **Marcas y Productos Principales** (Ej: '¿Cuáles son tus principales productos?', '¿Qué marcas manejas?')
    - **Categorías de Productos** (Ej: '¿Qué categorías de alimentos tienen?')
    - **Contacto** (Ej: '¿Cuál es el teléfono de servicio al cliente?', 'email de soporte')
    - **Horarios de Atención**
    - **NIT de la empresa**
    - **Sedes y Ubicaciones** (Ej: '¿Dónde están las sedes de Cali?', '¿Cuántas plantas tienen?')
    - **Metas de Sostenibilidad** (Ej: '¿Cuál es la meta de reducción de carbono?')
    - **Datos Generales** (Ej: '¿Quién es el presidente?', '¿Cuándo se fundó?')

**Instrucciones de Enrutamiento:**

1.  **Analiza la pregunta del usuario.**
2.  **Compara** la pregunta con la lista de datos fácticos de `search_structured_data`. Si coincide, úsala.
3.  Si la pregunta es abierta y no pide un dato fáctico, usa `consult_knowledge_base`.
4.  **Llama a UNA SOLA herramienta** si es necesario.
5.  **Argumentos para `consult_knowledge_base`:**
    - `question`: La pregunta actual del usuario.
    - `conversation_history`: Para este argumento, DEBES pasar la conversación que has tenido HASTA AHORA, convertida a una lista de diccionarios (json).
    - **Ejemplo de cómo el LLM debe pasar el historial:**
      `[{"type": "human", "content": "Hola"}, {"type": "ai", "content": "Hola, ¿en qué puedo ayudarte?"}]`
6.  **Argumentos para `search_structured_data`:**
    - `pregunta_clave`: Pasa una clave simple.
    - Ej: Si el usuario dice "¿A qué hora atienden?", llama con `pregunta_clave="horarios_atencion"`.
    - Ej: Si el usuario dice "¿Cuáles son sus productos?", llama con `pregunta_clave="productos_marcas"`.
7.  **Charla Casual:** Si la pregunta es un saludo, una despedida o una charla casual (Ej: "Hola", "Gracias", "¿Cómo estás?"), 
    NO uses ninguna herramienta. Responde directamente como un asistente amigable.

# --- NUEVA SECCIÓN: LÓGICA DE FALLBACK (Actualizada y más estricta) ---

8.  **Instrucción de Fallback (MUY IMPORTANTE):**
    Tu objetivo principal es conseguir la respuesta para el usuario.
    
    **CASO 1: Si `search_structured_data` falla:**
    Si llamas a `search_structured_data` y el resultado es:
    - un **error** (ej. `{"error": "No se encontró"}`)
    - un **resultado vacío** (ej. `[]` o `{}`)
    
    **NO TE RINDAS Y NO PIDAS DISCULPAS AÚN.**
    
    **ES TU OBLIGACIÓN** re-evaluar la pregunta. Piensa: "¿Pudo haber sido una pregunta abierta? ¿La otra herramienta (`consult_knowledge_base`) podría tener la respuesta?".
    Si la pregunta es ambigua o general (como 'háblame de los productos'), **DEBES LLAMAR** a la segunda herramienta (`consult_knowledge_base`) para hacer un segundo intento.

    **CASO 2: Si `consult_knowledge_base` falla:**
    Del mismo modo, si llamas a `consult_knowledge_base` (RAG) y el resultado es 'La información solicitada no se encuentra en mi base de conocimiento' o un error, **NO TE RINDAS AÚN**.
    Re-evalúa la pregunta. Piensa: '¿Quizás esta era una pregunta fáctica y me equivoqué?'
    Si la pregunta *podría* responderse con un dato fáctico (ej. '¿Cuál es el NIT?'), **DEBES LLAMAR** a `search_structured_data` como segundo intento.

    **Solo pide disculpas al usuario si AMBAS herramientas han fallado** y estás seguro de que no tienes la información.

    **Ejemplo de Flujo de Fallback (Caso 1):**
    1.  Usuario: "¿Cuáles son sus principales productos?"
    2.  Agente (Tú): (Piensa: 'Productos está en datos fácticos.') -> Llama a `search_structured_data(pregunta_clave='productos_marcas')`
    3.  ToolNode: (Devuelve: `{"productos": []}` o `{"error": "no encontrado"}`)
    4.  Agente (Tú): (Ves el resultado vacío/error. Piensas: 'Ok, el dato fáctico falló. Pero "productos" es una pregunta general. El RAG (`consult_knowledge_base`) DEBE saber algo.') -> **Llama a `consult_knowledge_base(question='¿Cuáles son sus principales productos?', conversation_history=...)`**
    5.  ToolNode: (Devuelve la respuesta del RAG...)
    6.  Agente (Tú): (Formulas la respuesta final al usuario.)

# --- FIN DE LA NUEVA SECCIÓN ---
"""


llm_router = ChatOpenAI(model="gpt-4o", api_key=API_KEY, temperature=0)
llm_with_tools = llm_router.bind_tools(tools)


def _convert_state_messages_to_objects(messages: List[dict]) -> List[BaseMessage]:
    """
    Convierte la lista de diccionarios de mensajes del estado a una lista de objetos BaseMessage.
    """
    current_messages = []
    for msg in messages:
        if isinstance(msg, dict):
            msg_type = msg.get("type")
            if msg_type == 'human':
                current_messages.append(HumanMessage(content=msg['content']))
            elif msg_type == 'ai':
                tool_calls = msg.get('tool_calls', [])
                if tool_calls:
                    parsed_tool_calls = [
                        {
                            "name": call.get("name"),
                            "args": call.get("args"),
                            "id": call.get("id"),
                            "type": "tool_call"
                        } for call in tool_calls
                    ]
                    current_messages.append(AIMessage(content=msg['content'], tool_calls=parsed_tool_calls))
                else:
                    current_messages.append(AIMessage(content=msg['content']))
            elif msg_type == 'tool':
                current_messages.append(
                    ToolMessage(content=msg['content'], tool_call_id=msg['tool_call_id'], name=msg.get('name', 'tool'))
                )
        elif isinstance(msg, BaseMessage):
            current_messages.append(msg)
    return current_messages


def agent_node(state: AgentState):
    """
    El nodo principal del agente. Decide si llamar a una herramienta o responder directamente.
    """
    logger.info("🤖 Iniciando nodo agente (router)")
    messages = state['messages']
    
    messages_for_llm = [SystemMessage(content=AGENT_SYSTEM_PROMPT)]
    
    current_messages = _convert_state_messages_to_objects(messages)
            
    messages_for_llm.extend(current_messages)

    try:
        logger.info("🔄 Invocando LLM con herramientas...")
        response = llm_with_tools.invoke(messages_for_llm)
        logger.info(f"✅ Respuesta LLM obtenida: {response.content[:50]}...")
        if response.tool_calls:
            logger.info(f"🔧 Llamadas a herramientas detectadas: {len(response.tool_calls)}")
            
    except Exception as e:
        logger.error(f"❌ Error invocando LLM: {e}")
        response = AIMessage(content="Lo siento, tuve un error al procesar tu solicitud.")

    response_dict = {
        "type": "ai",
        "content": response.content,
        "tool_calls": response.tool_calls or [] 
    }

    return {"messages": [response_dict]}


def tool_node_wrapper(state: AgentState):
    """
    Un wrapper para el ToolNode que maneja y formatea la salida de la herramienta.
    """
    logger.info("🔧 Iniciando nodo de herramientas")
    
    messages = state['messages']
    current_messages = _convert_state_messages_to_objects(messages)
    
    try:
        tool_results = tool_node.invoke(current_messages)
    except Exception as e:
        logger.error(f"❌ Error ejecutando herramientas: {e}")
        last_message = state['messages'][-1]
        tool_call_id = last_message.get('tool_calls', [{}])[0].get('id', 'error_no_id')
        tool_results = [
            ToolMessage(
                content=f"Error al ejecutar la herramienta: {e}", 
                tool_call_id=tool_call_id,
                name="error_tool"
            )
        ]
        
    tool_result_dicts = []
    for tool_msg in tool_results:
        logger.info(f"📋 Resultado de {tool_msg.name}: {tool_msg.content[:100]}...")
        tool_result_dicts.append({
            "type": "tool",
            "content": tool_msg.content,
            "tool_call_id": tool_msg.tool_call_id,
            "name": tool_msg.name
        })
    
    return {"messages": tool_result_dicts}


def should_call_tools(state: AgentState) -> str:
    """
    Decide si el grafo debe llamar a las herramientas o terminar el turno.
    """
    last_message = state['messages'][-1]
    
    if last_message.get('tool_calls'):
        logger.info("🔧 Decisión: Llamar herramientas")
        return "call_tool"
    
    logger.info("✅ Decisión: Terminar turno")
    return "end_turn"


logger.info("🔨 Construyendo el grafo de LangGraph...")

workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
workflow.add_node("tool_node", tool_node_wrapper)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_call_tools,
    {
        "call_tool": "tool_node",
        "end_turn": END
    }
)

workflow.add_edge("tool_node", "agent")

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

logger.info("✅ Grafo LangGraph compilado y listo")


def run_conversation_turn(app, session_id: str, user_input: str):
    """
    Ejecuta un solo turno de la conversación.
    """
    logger.info(f"👤 Usuario: {user_input}")
    
    config = {"configurable": {"thread_id": session_id}}
    
    input_message = {"type": "human", "content": user_input}
    
    final_state = app.invoke(
        {"messages": [input_message]},
        config=config
    )
    
    final_response = final_state['messages'][-1]
    
    logger.info(f"🤖 Respuesta del agente: {final_response['content']}")
    return final_response['content']


if __name__ == "__main__":
    logger.info("🧪 Iniciando pruebas del agente conversacional")
    
    session_id = f"terminal_session_{uuid.uuid4()}" 
    
    logger.info("📝 Prueba 1: Consulta de datos estructurados (NIT)")
    run_conversation_turn(app, session_id, "¿Cuál es el NIT de la empresa?")
    
    logger.info("📝 Prueba 2: Consulta RAG (misión y visión)")
    run_conversation_turn(app, session_id, "Háblame sobre la misión y visión de Colombina")
    
    logger.info("📝 Prueba 3: Memoria conversacional (seguimiento)")
    run_conversation_turn(app, session_id, "¿Y cuáles son sus valores principales?")
    
    logger.info("📝 Prueba 4: Fallback (datos → RAG)")
    run_conversation_turn(app, session_id, "¿Cuál es la política de Colombina sobre el uso del agua?")

    logger.info("📝 Prueba 5: Fallback (RAG → datos)")
    run_conversation_turn(app, session_id, "Me gustaría saber el número de identificación fiscal de la empresa, por favor.")

    logger.info("🔍 Estado final de la memoria")
    final_memory_state = app.get_state(config={"configurable": {"thread_id": session_id}})
    logger.debug(json.dumps(final_memory_state.to_json(), indent=2, ensure_ascii=False))
    logger.info("📊 Memoria guardada exitosamente")