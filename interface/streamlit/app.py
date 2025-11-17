"""Aplicación Streamlit para el Agente Conversacional de Colombina con memoria, RAG, y herramientas de datos estructurados - Segunda entrega."""

import sys
import uuid
import streamlit as st
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.logging_util.logger import get_logger

logger = get_logger()

try:
    from RAG.agent.colombina_agent import app as agent_colombina
    from RAG.agent.colombina_agent import AgentState
    logger.info("✅ Agente principal cargado exitosamente")

except ImportError as e:
    logger.error(f"❌ Error fatal: No se pudo importar el agente: {e}")
    st.error(f"Error fatal: No se pudo importar el agente: {e}")
    st.info("Asegúrate de que 'agente_principal.py', 'tool_rag.py', y 'tool_datos_estructurados.py' estén en la misma carpeta.")
    st.stop()


st.set_page_config(page_title="Agente Colombina (Taller 2)", layout="wide")
st.title("🤖 Agente Conversacional de Colombina")
st.caption("Con memoria, RAG, y herramientas de datos estructurados.")


if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    logger.info(f"🆔 Nuevo session_id generado: {st.session_state.session_id}")


LANGGRAPH_CONFIG = {"configurable": {"thread_id": st.session_state.session_id}}

with st.sidebar:
    st.header("Control de Memoria")
    st.info(f"**ID de Sesión Actual:**\n`{st.session_state.session_id}`")
    st.write("El agente recordará la conversación mientras esta sesión esté activa.")
    
    if st.button("Iniciar Nuevo Chat (Limpiar Memoria)"):
        logger.info(f"🧹 Limpiando memoria para sesión: {st.session_state.session_id}")
        
        try:
            agent_colombina.get_state(LANGGRAPH_CONFIG)
            agent_colombina.update_state(
                LANGGRAPH_CONFIG, 
                AgentState(messages=[])
            )
            
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())
            logger.info(f"🆔 Nuevo session_id generado: {st.session_state.session_id}")
            st.success("¡Memoria limpiada! Listo para un nuevo chat.")
            st.rerun()
        except Exception as e:
            logger.error(f"❌ Error al limpiar memoria: {e}")
            st.error(f"Error al limpiar la memoria: {e}")


if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(
        {"role": "assistant", "content": "¡Hola! Soy el agente de Colombina. ¿Cómo puedo ayudarte hoy?"}
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu pregunta aquí... (ej: ¿Cuál es el NIT?)"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando y buscando..."):
            try:
                logger.info(f"👤 Usuario pregunta: {prompt}")
                input_message = {"type": "human", "content": prompt}
                
                final_state = agent_colombina.invoke(
                    {"messages": [input_message]},
                    config=LANGGRAPH_CONFIG
                )
                
                final_response_dict = final_state['messages'][-1]
                
                response_content = final_response_dict.get('content', 'Lo siento, no obtuve una respuesta.')

                st.session_state.messages.append({"role": "assistant", "content": response_content})
                st.markdown(response_content)
                logger.info("✅ Respuesta entregada al usuario")

            except Exception as e:
                error_msg = f"❌ Ocurrió un error al invocar al agente: {e}"
                logger.error(f"{error_msg}")
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})