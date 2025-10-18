import streamlit as st
from llm.FAQ.faq_ollama import generate_faqs
from llm.QA.qa_ollama import process_question
from llm.llm_openai import procesar_pregunta_colombina
from llm.summary.generate_summary import generate_summary

st.set_page_config(page_title="Centro de Información Colombina", page_icon="🍭", layout="wide")

st.title("🍭 Centro de Información Colombina")
    
st.markdown("""
**Bienvenido al Centro de Información integral de Colombina**

Explora diferentes aspectos de la información corporativa a través de las siguientes herramientas:
""")

# Crear pestañas
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Consulta Q&A", 
    "❓ Preguntas Frecuentes", 
    "📋 Resumen Ejecutivo", 
    "💬 Chatbot Interactivo"
])

with st.sidebar:
    st.header("🛠️ Parámetros de Configuración")
    
    temperature = st.slider(
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
    
    st.divider()

    model_choice = st.selectbox(
        "**Modelo Ollama**",
        ["gpt-oss:20b"],
        index=0
    )


with tab1:
    st.subheader("🔍 Sistema de Consulta Q&A")
    st.markdown("""
    Realiza preguntas específicas sobre Colombina y obtén respuestas basadas en la base de conocimiento oficial.
    """)
    
    st.markdown("🚀 **Preguntas de Ejemplo**")
    example_questions = [
        "¿Cómo se llama el programa de Colombina para acompañar a sus proveedores y emprendedores?",
        "Qué porcentaje de la energía eléctrica que utiliza Colombina en sus operaciones en Colombia proviene de fuentes renovables?",
        "¿Qué es Colombina Energía S.A.S. E.S.P. y cuál es su función principal?",
        "¿Cuáles son los principales logros de Colombina en materia de sostenibilidad relacionados con la energía y el agua?",
        "¿Cuándo y cómo fue fundada Colombina?",
        "¿En cuántos países tiene presencia la empresa actualmente?",
        "¿Cuál fue el producto icónico que impulsó la expansión internacional de Colombina?",
        "¿Logros sostenibilidad energía y agua?",
        "¿Qué programas sociales lidera la Fundación Colombina?",
        "¿Qué iniciativas promueve Colombina para fomentar la equidad de género en su organización?"
    ]
    
    selected_question = st.selectbox("Selecciona una pregunta de ejemplo:", example_questions)

    question = selected_question
    
    if st.button("🔍 Buscar Respuesta", disabled=not question):
        with st.spinner("Procesando pregunta..."):
            try:
                answer = process_question(model_choice, question, temperature, top_p)
                
                st.success("✅ Respuesta encontrada:")
                st.write(answer)
                
            except Exception as e:
                st.error(f"❌ Error procesando pregunta: {e}")


with tab2:
    st.subheader("❓ Generador de Preguntas Frecuentes")
    st.markdown("""
    **Genera automáticamente preguntas frecuentes basadas en la información disponible de Colombina.**
    
    Esta herramienta analiza toda la base de conocimiento y crea preguntas que comúnmente 
    podrían hacer clientes, proveedores o colaboradores.
    """)
    
    if st.button("🎯 Generar FAQs"):
        with st.spinner("Analizando base de conocimiento y generando preguntas frecuentes..."):
            try:
                faqs = generate_faqs(model_choice, temperature, top_p)
                
                st.success("✅ Preguntas frecuentes generadas:")
                st.markdown(faqs)
                
                st.download_button(
                    label="📥 Descargar FAQs",
                    data=faqs,
                    file_name="faqs_colombina.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"❌ Error generando FAQs: {e}")


with tab3:
        st.subheader("📋 Generador de Resumen Ejecutivo")
        st.markdown("""
        **Genera un resumen ejecutivo completo de toda la información disponible sobre Colombina.**
        
        Este resumen incluye aspectos clave como historia, productos, sostenibilidad, 
        operaciones y logros principales de la empresa.
        """)
        
        if st.button("📊 Generar Resumen Ejecutivo"):
            with st.spinner("Analizando información y generando resumen ejecutivo..."):
                try:
                    summary = generate_summary(model_choice, temperature, top_p)

                    st.success("✅ Resumen ejecutivo generado:")
                    st.markdown(summary)
                    
                    st.download_button(
                        label="📥 Descargar Resumen",
                        data=summary,
                        file_name="resumen_ejecutivo_colombina.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error generando resumen: {e}")


with tab4:
    st.subheader("💬 Chatbot Interactivo Colombina")
    st.markdown("""
    **Conversación interactiva con el asistente virtual de Colombina usando OpenAI.**
    
    Esta es una experiencia de chat completa donde puedes mantener conversaciones 
    naturales sobre productos, servicios e información de Colombina.
    """)

    user_input = st.chat_input("Pregúntame sobre productos Colombina, ingredientes, disponibilidad... 🍭")

    if user_input:        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.spinner("Pensando..."):
            try:
                respuesta = procesar_pregunta_colombina(user_input, temperature, top_p)
                
                with st.chat_message("assistant"):
                    st.markdown(respuesta)
                
            except Exception as e:
                error_message = f"⚠️ Ocurrió un error: {e}"
                
                with st.chat_message("assistant"):
                    st.markdown(error_message)