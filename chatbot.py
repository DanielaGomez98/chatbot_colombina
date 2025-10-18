import streamlit as st
from llm.QA.qa_openai import procesar_pregunta_colombina

# Configuración de la página
st.set_page_config(page_title="Chatbot Colombina", page_icon="🍭", layout="wide")

# Título y descripción
st.title("🍭 Asistente Virtual de Colombina")

st.markdown("""
¡Bienvenido al asistente virtual de **Colombina**! 

**¿Cómo funciona?**
- 💬 **Conversación simple**: Haz preguntas sobre productos, servicios o información de Colombina
- 🍬 **Conocimiento especializado**: Información actualizada sobre dulces, chocolates y productos Colombina
- ⚡ **Respuestas rápidas**: Obtén información instantánea sobre lo que necesites

**¡Comienza** preguntando sobre productos, ingredientes, disponibilidad o cualquier tema relacionado con Colombina!
""")

with st.sidebar:
    st.header("🛠️ Parámetros de Configuración")
    
    # Parámetros del modelo
    temperatura = st.slider(
        "🌡️ Temperatura",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1,
        help="Controla la creatividad de las respuestas. Valores más altos = más creatividad"
    )
    
    top_p = st.slider(
        "🎯 Top P",
        min_value=0.0,
        max_value=1.0,
        value=0.9,
        step=0.05,
        help="Controla la diversidad de las respuestas. Valores más bajos = más enfoque"
    )
    
    # Separador
    st.divider()
    
    if st.session_state.get("messages", []):
        if st.button("🗑️ Limpiar Conversación", 
                     type="secondary", 
                     help="Borrar todo el historial de la conversación",
                     use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# Inicializar el historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de conversación
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input del usuario
user_input = st.chat_input("Pregúntame sobre productos Colombina, ingredientes, disponibilidad... 🍭")

if user_input:
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Procesar respuesta del asistente
    with st.spinner("Pensando..."):
        try:
            # Aquí llamas a tu función real del chatbot
            respuesta = procesar_pregunta_colombina(user_input, temperatura, top_p)
            
            # Mostrar respuesta del asistente
            with st.chat_message("assistant"):
                st.markdown(respuesta)
            
            # Agregar respuesta al historial
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
            
        except Exception as e:
            error_message = f"⚠️ Ocurrió un error: {e}"
            
            with st.chat_message("assistant"):
                st.markdown(error_message)
            
            st.session_state.messages.append({"role": "assistant", "content": error_message})