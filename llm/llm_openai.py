import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()


def procesar_pregunta_colombina(pregunta: str, temperatura: float = 0.5, top_p: float = 0.9):
    """
    Procesa la pregunta del usuario usando el modelo OpenAI con parámetros configurables.
    
    Args:
        pregunta (str): La pregunta del usuario
        temperatura (float): Controla la creatividad (0.0 - 1.0)
        top_p (float): Controla la diversidad (0.0 - 1.0)
    
    Returns:
        str: Respuesta del modelo
    """
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return """⚠️ **Falta la API Key de OpenAI**
            
Para configurar tu API Key:
1. Obtén tu API Key en: https://platform.openai.com/api-keys
2. Crea un archivo `.env` en la carpeta del proyecto
3. Agrega: `OPENAI_API_KEY=tu_api_key_aqui`
4. O ejecuta: `export OPENAI_API_KEY=tu_api_key_aqui`"""
        
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=temperatura,
            top_p=top_p,
            api_key=api_key
        )
        
        template = """Eres un asistente virtual especializado en la empresa Colombina, líder en dulces y confitería en Colombia y Latinoamérica. 
        
Responde de manera amigable, profesional y con conocimiento sobre:
- Productos Colombina (dulces, chocolates, confitería)
- Historia y valores de la empresa
- Disponibilidad de productos
- Ingredientes y información nutricional
- Promociones y novedades

Pregunta: {question}
Respuesta:"""
        
        prompt = PromptTemplate.from_template(template)
        
        chain = prompt | llm
        
        respuesta = chain.invoke({"question": pregunta})
        
        return respuesta.content.strip()
        
    except Exception as e:
        return f"⚠️ Error al procesar la pregunta: {str(e)}"