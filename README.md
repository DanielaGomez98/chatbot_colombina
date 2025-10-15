# 🍭 Chatbot Colombina

Un asistente virtual especializado en la empresa **Colombina**, líder en dulces y confitería en Colombia y Latinoamérica. Este chatbot utiliza tecnología de inteligencia artificial para brindar información sobre productos, servicios e historia de la empresa.

## 🌟 Características

- **💬 Conversación Natural**: Interfaz de chat intuitiva y amigable
- **🍬 Conocimiento Especializado**: Información específica sobre productos Colombina
- **⚡ Respuestas Rápidas**: Procesamiento inmediato de consultas usando GPT-4o
- **🛠️ Parámetros Configurables**: Control de temperatura y top_p del modelo
- **🎨 Interfaz Moderna**: Desarrollado con Streamlit
- **🧹 Conversaciones Sin Memoria**: Cada consulta es independiente, ideal para uso básico

## 🚀 Tecnologías Utilizadas

- **Python 3.13+**
- **Streamlit** - Interfaz de usuario
- **LangChain** - Framework para LLMs
- **OpenAI GPT-4o** - Modelo de lenguaje
- **python-dotenv** - Gestión de variables de entorno

## 📋 Requisitos Previos

- Python 3.13 o superior
- API Key de OpenAI
- Conexión a internet

## 🔧 Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd chatbot_colombina
```

2. **Instalar dependencias**
```bash
uv venv
source .venv/bin/activate
uv pip install -r pyproject.toml
```

3. **Configurar API Key de OpenAI**

   **Opción A: Archivo .env**
   ```bash
   # Crear archivo .env en la raíz del proyecto
   echo "OPENAI_API_KEY=tu_api_key_aqui" > .env
   ```

   **Opción B: Variable de entorno**
   ```bash
   export OPENAI_API_KEY=tu_api_key_aqui
   ```

   > 💡 Obtén tu API Key en: https://platform.openai.com/api-keys

## 🏃‍♂️ Uso

1. **Ejecutar la aplicación**
```bash
streamlit run chatbot.py
```

2. **Abrir en el navegador**
   - La aplicación se abrirá automáticamente en `http://localhost:8501`

3. **Usar el chatbot**
   - Escribe preguntas sobre productos Colombina
   - Ajusta los parámetros en el sidebar si deseas
   - Limpia la conversación cuando quieras empezar de nuevo
   - ¡Disfruta de la conversación!

## 📁 Estructura del Proyecto

```
chatbot_colombina/
├── chatbot.py              # Interfaz principal de Streamlit
├── llm/
│   ├── __init__.py         # Inicializador del paquete
│   └── llm.py              # Lógica del modelo LLM y prompts
├── preprocessing/          # Módulos de preprocesamiento (en desarrollo)
├── web_scraping/          # Módulos de web scraping (en desarrollo)
├── pyproject.toml         # Configuración del proyecto y dependencias
├── .env                   # Variables de entorno (no incluir en git)
├── .gitignore             # Archivos a ignorar
├── .gitattributes         # Configuración de Git
├── LICENSE                # Licencia Apache 2.0
└── README.md              # Este archivo
```

## ⚙️ Configuración

### Parámetros del Modelo (Sidebar)

- **🌡️ Temperatura (0.0-1.0)**: Controla la creatividad de las respuestas
  - Valores bajos = respuestas más conservadoras
  - Valores altos = respuestas más creativas
  - Valor por defecto: 0.5

- **🎯 Top P (0.0-1.0)**: Controla la diversidad de las respuestas
  - Valores bajos = más enfoque en palabras probables
  - Valores altos = mayor diversidad de vocabulario
  - Valor por defecto: 0.9

### Funcionalidades de la Interfaz

- **🗑️ Limpiar Conversación**: Reinicia el historial de chat
- **💬 Historial Visual**: Muestra toda la conversación actual
- **⚡ Indicador de Carga**: Spinner mientras procesa la respuesta

## 💬 Ejemplos de Preguntas

- "¿Qué productos fabrica Colombina?"
- "Cuéntame sobre la historia de Colombina"
- "¿Qué ingredientes tienen los Bon Bon Bum?"
- "¿Dónde puedo comprar productos Colombina?"
- "¿Tienen productos sin azúcar?"
- "¿Cuáles son los dulces más populares de Colombina?"

## 🛠️ Desarrollo

### Arquitectura del Código

- [`chatbot.py`](chatbot.py): Contiene toda la interfaz de Streamlit y lógica de sesión
- [`llm/llm.py`](llm/llm.py): Maneja la lógica del modelo LLM, prompts y comunicación con OpenAI

### Función Principal

La función [`procesar_pregunta_colombina`](llm/llm.py) en [`llm/llm.py`](llm/llm.py) es el corazón del chatbot:
- Valida la API Key de OpenAI
- Configura el modelo GPT-4o con parámetros personalizables
- Utiliza un prompt especializado para Colombina
- Maneja errores y proporciona mensajes informativos

### Agregar Nuevas Funcionalidades

1. **Modificar el prompt**: Editar el template en [`llm/llm.py`](llm/llm.py)
2. **Cambiar modelo**: Modificar el parámetro `model` en `ChatOpenAI`
3. **Agregar parámetros**: Incluir nuevos sliders en el sidebar de [`chatbot.py`](chatbot.py)
4. **Integrar preprocesamiento**: Desarrollar módulos en la carpeta `preprocessing/`
5. **Agregar web scraping**: Implementar funciones en la carpeta `web_scraping/`

## 🔒 Seguridad

- ✅ Las API Keys se manejan como variables de entorno
- ✅ No se almacenan credenciales en el código
- ✅ Archivo [`.env`](.env) incluido en [`.gitignore`](.gitignore)
- ✅ Licencia Apache 2.0 para uso comercial y educativo

## 🐛 Solución de Problemas

### Error: "Falta la API Key de OpenAI"
- Verifica que tu API Key esté configurada correctamente
- Asegúrate de que el archivo `.env` esté en la raíz del proyecto
- Comprueba que la variable se llame exactamente `OPENAI_API_KEY`

### Error: "Connection refused" o errores de red
- Verifica tu conexión a internet
- Comprueba que tu API Key sea válida y tenga créditos
- Verifica que no haya restricciones de firewall

### La aplicación no inicia
- Verifica que tengas Python 3.13+
- Instala todas las dependencias: `pip install -e .`
- Asegúrate de estar en el directorio correcto del proyecto

### Errores con dependencias
- Actualiza pip: `pip install --upgrade pip`
- Reinstala las dependencias: `pip install --force-reinstall -e .`

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia Apache 2.0. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🚧 Estado del Proyecto

**Versión actual: 0.1.0**

### Completado ✅
- Interfaz básica de Streamlit
- Integración con OpenAI GPT-4o
- Parámetros configurables
- Prompt especializado para Colombina
- Manejo de errores

### En Desarrollo 🚧
- Módulos de preprocesamiento
- Sistema de web scraping
- Base de datos de conocimiento de Colombina
- Funcionalidades avanzadas de RAG

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📞 Contacto

Para preguntas o sugerencias sobre este chatbot, por favor contacta al equipo de desarrollo.

---

**¡Disfruta conversando con el asistente virtual de Colombina! 🍭**