# 🍭 Centro de Información Colombina

Un sistema integral de inteligencia artificial especializado en **Colombina**, desarrollado en tres entregas que evolucionaron desde un chatbot básico hasta un agente conversacional avanzado con API REST, despliegue en la nube y trazabilidad completa.

## 📋 Evolución del Proyecto

### 📦 Primera Entrega: Fundación del Sistema
**Objetivo:** Crear la infraestructura base de datos y análisis de información corporativa

### 📦 Segunda Entrega: Agente Conversacional Avanzado  
**Objetivo:** Implementar un sistema RAG completo con memoria conversacional y herramientas especializadas

### 📦 Tercera Entrega: API REST y Despliegue en Producción
**Objetivo:** Crear una API REST profesional, múltiples interfaces de usuario y desplegar el sistema en la nube con trazabilidad completa

---

## 🌟 Características por Entrega

### 🔹 Primera Entrega - Infraestructura y Análisis

#### Funcionalidades Implementadas:
- **🕷️ Web Scraping Completo**: Extracción automática del sitio oficial de Colombina
- **📄 Procesamiento de Documentos**: Sistema de limpieza y estructuración de contenido
- **📊 Análisis de Contenido**: Generación de insights y métricas
- **❓ Sistema de FAQs**: Generación automática de preguntas frecuentes
- **📋 Resumen Ejecutivo**: Análisis integral de información corporativa
- **🔄 Pipeline de Chunking**: División inteligente de contenido
- **📚 Base de Conocimiento**: Estructuración de información corporativa
- **🎯 Interfaz Streamlit Básica**: Chatbot simple con 4 pestañas (chatbot.py)
- **🤖 Chatbot con Modelo Local**: Sistema Q&A usando Ollama sin vectorización

#### Módulos Desarrollados:
```
├── web_scraping/                       # Sistema de extracción web
│   ├── scripts/
│   │   ├── extract_colombina_links.py
│   │   └── advanced_scraper.py         # Scraper principal
│   ├── colombina_advanced/             # Datos extraídos
│   │   └── data/
│   │       ├── noticias/
│   │       └── otros/
│   └── pdf_extraction/                 # PDFs procesados
│       └── markdown/
│
├── preprocessing/                      # Procesamiento de datos
│   ├── clean_md_files.py               # Limpieza de markdown
│   ├── selected_md_files/              # Archivos seleccionados
│   └── cleaned_md_files/               # Archivos procesados
│
├── chunking/                           # División de contenido
│   ├── chunking.py                     # Generación de chunks
│   └── chunks.json                     # Chunks para RAG
│
├── knowledge_base/                     # Base de conocimiento
│   ├── knowledge_base.txt              # Base original
│   ├── improved_knowledge_base.txt     # Base mejorada
│   └── clean_kb.py                     # Script de limpieza
│
├── llm/                                # Módulos de IA básicos
│   ├── llm_openai.py                   # OpenAI GPT-4o integration
│   ├── FAQ/
│   │   └── faq_openai.py               # Generador de FAQs
│   ├── QA/
│   │   └── qa_ollama.py                # Sistema Q&A con Ollama
│   └── summary/
│       └── generate_summary.py         # Generador de resúmenes
│
├── logging_util/                       # Sistema de logging
│   ├── logger.py                       # Configuración de logs
│   └── logs/                           # Archivos de log
│
├──tests/                               # 🧪 Pruebas y análisis
│   └── Taller1.ipynb                   # Notebooks de evaluación
│
├── requirements.txt                    # 📦 Dependencias del proyecto
├── pyproject.toml                      # ⚙️ Configuración del proyecto
└── chatbot.py                          # Interfaz Streamlit básica (4 pestañas)
```

### 🔹 Segunda Entrega - Agente Conversacional RAG

#### Nuevas Funcionalidades:
- **🤖 Agente Conversacional**: Sistema LangGraph con memoria persistente
- **🔍 Sistema RAG Avanzado**: Retrieval-Augmented Generation con ChromaDB
- **🛠️ Herramientas Especializadas**: Tools para datos estructurados y RAG
- **💭 Memoria Conversacional**: Contexto persistente entre sesiones
- **🔄 Sistema de Fallback**: Lógica inteligente entre herramientas
- **🎯 Interfaz Streamlit Avanzada**: Aplicación web con agente conversacional (app.py)

#### Nuevos Módulos:
```
├── RAG/                                # 🆕 Sistema RAG completo
│   ├── agent/                          # Agente conversacional
│   │   ├── colombina_agent.py          # Agente principal LangGraph
│   │   ├── tool_rag.py                 # Herramienta RAG
│   │   └── tool_structured_data.py     # Herramienta datos estructurados
│   │   └── company_data.json           # 📋 Base de datos JSON estructurada
│   ├── vector_db/                      # Base de datos vectorial
│   │   └── load_data.py                # Carga de embeddings
│   └── chroma_db/                      # ChromaDB persistente
└── app.py                              # 🆕 Interfaz Streamlit
```

### 🔹 Tercera Entrega - API REST y Despliegue en Producción

#### Nuevas Funcionalidades:
- **🌐 API REST Completa**: FastAPI con documentación automática (Swagger/ReDoc)
- **🚀 Despliegue en Railway**: Sistema en producción 24/7 accesible públicamente
- **🔍 Trazabilidad con LangSmith**: Monitoreo completo de conversaciones y costos
- **🎨 Múltiples Interfaces**: HTML vanilla y Streamlit
- **📊 Gestión de Sesiones**: Sistema robusto de identificación de usuarios
- **⚙️ Configuración Dinámica**: Parámetros personalizables del modelo (temperature, top_p, max_tokens)
- **🔒 Mejores Prácticas**: CORS, variables de entorno, logging profesional
- **📈 Healthchecks**: Monitoreo de estado del servicio

#### Nuevos Módulos:
```
├── api/                                # 🆕 API REST con FastAPI
│   ├── __init__.py
│   ├── main.py                         # Aplicación FastAPI principal
│   └── README.md                       # Documentación de la API
│
├── interface/                          # 🆕 Múltiples interfaces de usuario
│   ├── html/                           # Interfaz web vanilla
│   │   ├── index.html                  # HTML principal
│   │   ├── styles.css                  # Estilos personalizados
│   │   └── app.js                      # Lógica del cliente
│   └── streamlit/                      # Interfaces Streamlit
│       ├── app.py                      # App Streamlit con API
│       └── chatbot.py                  # Chatbot Streamlit legacy
│
├── api_server.py                       # 🆕 Servidor de producción
├── .env.example                        # 🆕 Plantilla de variables de entorno
├── Procfile                            # 🆕 Comando de inicio para Railway
└── railway.json                        # 🆕 Configuración de Railway (healthcheck, restart policy)
```

#### Configuración de Despliegue:
```bash
# Variables de entorno requeridas
OPENAI_API_KEY=sk-proj-...             # API key de OpenAI
PORT=8000                               # Puerto (Railway lo asigna automáticamente)

# Variables de entorno opcionales (LangSmith)
LANGCHAIN_TRACING_V2=true               # Activar trazabilidad
LANGCHAIN_API_KEY=lsv2_pt_...          # API key de LangSmith
LANGCHAIN_PROJECT=colombina-chatbot     # Nombre del proyecto
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

---

## 🚀 Tecnologías Utilizadas

### Primera Entrega - Fundación
- **Python 3.13+** - Lenguaje base
- **Selenium + BeautifulSoup** - Web scraping
- **OpenAI GPT-4o** - Generación de contenido
- **Ollama (gpt-oss:20b)** - Modelos locales sin vectorización
- **Streamlit** - Interfaz web básica (chatbot.py)
- **JSON/CSV** - Almacenamiento de datos
- **Logging personalizado** - Trazabilidad

### Segunda Entrega - Avances
- **LangChain + LangGraph** - Framework de agentes
- **ChromaDB** - Base de datos vectorial
- **OpenAI Embeddings** - Vectorización de texto
- **Streamlit Avanzado** - Interfaz web con agente (app.py)
- **Memory Persistence** - Gestión de estado
- **Tool Orchestration** - Coordinación de herramientas

### Tercera Entrega - Producción
- **FastAPI** - Framework web moderno y rápido
- **Uvicorn** - Servidor ASGI de alto rendimiento
- **Railway** - Plataforma de despliegue en la nube
- **LangSmith** - Trazabilidad y monitoreo de LLMs
- **CORS Middleware** - Seguridad y acceso cross-origin
- **Pydantic** - Validación de datos y modelos
- **HTML/CSS/JavaScript** - Interfaz web nativa
- **Environment Variables** - Configuración segura
- **Nixpacks** - Sistema de build automático de Railway
- **Healthchecks** - Monitoreo de disponibilidad del servicio

---

## 🔧 Instalación y Configuración

### Requisitos Previos
- Python 3.13 o superior
- API Key de OpenAI (obligatoria)
- API Key de LangSmith (opcional, para trazabilidad)
- Ollama instalado (opcional, para funciones de primera entrega)
- Chrome/Chromium (para web scraping)

### Instalación
```bash
# Clonar repositorio
git clone <url-del-repositorio>
cd chatbot_colombina

# Crear entorno virtual
uv venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instalar dependencias
uv pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env y agregar tus API keys

# Variables obligatorias en .env:
# OPENAI_API_KEY=sk-proj-tu-key-aqui

# Variables opcionales para trazabilidad:
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=lsv2_pt_tu-key-aqui
# LANGCHAIN_PROJECT=colombina-chatbot
# LANGCHAIN_ENDPOINT=https://api.smith.langchain.com

# Instalar Ollama (opcional, para primera entrega)
ollama pull gpt-oss:20b
```

---

## 🏃‍♂️ Uso del Sistema

### 🌐 API REST en Producción (Tercera Entrega)

#### Despliegue en Railway
El sistema está desplegado en Railway y accesible públicamente 24/7.

**URL de producción**: `https://tu-app.railway.app` (configurar según tu deployment)

**Archivos de configuración Railway:**

1. **`Procfile`** - Define el comando de inicio:
   ```
   web: python api_server.py
   ```

2. **`railway.json`** - Configuración de despliegue:
   - Healthcheck en `/health`
   - Política de reintentos automáticos
   - Timeout de 300 segundos
   - Builder Nixpacks

3. **Variables de entorno en Railway** (configuradas en la plataforma):
   - `OPENAI_API_KEY` - Obligatoria
   - `LANGCHAIN_TRACING_V2` - Opcional
   - `LANGCHAIN_API_KEY` - Opcional
   - `LANGCHAIN_PROJECT` - Opcional
   - `PORT` - Asignada automáticamente por Railway

#### Endpoints Disponibles:

1. **Documentación Interactiva**
   - Swagger UI: `https://tu-app.railway.app/docs`
   - ReDoc: `https://tu-app.railway.app/redoc`

2. **Health Check**
   ```bash
   curl https://tu-app.railway.app/health
   # Respuesta: {"status":"healthy","version":"2.0.0"}
   ```

3. **Chat Endpoint**
   ```bash
   curl -X POST https://tu-app.railway.app/chat \
     -H "Content-Type: application/json" \
     -d '{
       "message": "¿Cuál es la misión de Colombina?",
       "session_id": "user-123",
       "temperature": 0.7,
       "top_p": 0.9,
       "max_tokens": 500
     }'
   ```

4. **Interfaz Web**
   - HTML: `https://tu-app.railway.app/interface`
   - Interfaz interactiva con diseño moderno

#### Ejecutar Localmente (Desarrollo)
```bash
# Opción 1: Usando el servidor de producción
python api_server.py
# Servidor en http://localhost:8000

# Opción 2: Usando uvicorn directamente
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Acceder a:
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - Interface: http://localhost:8000/interface
# - Health: http://localhost:8000/health
```

### 🎯 Agente Conversacional (Segunda Entrega)
```bash
# Interfaz principal Streamlit con agente RAG
streamlit run interface/streamlit/app.py
```
**Funcionalidades:**
- Conversación natural con memoria persistente
- Consultas sobre Colombina usando RAG
- Datos estructurados (contacto, horarios, NIT)
- Sistema de fallback inteligente

### 📊 Interfaces de Usuario

#### Interfaz HTML (Tercera Entrega)
Incluida en la API REST, accesible en `/interface`
- Diseño moderno y responsivo
- Chat en tiempo real
- Gestión automática de sesiones
- Sin necesidad de configuración adicional

#### Interfaz Streamlit Original
```bash
# Interfaz básica con 4 pestañas (modelo local sin RAG)
streamlit run interface/streamlit/chatbot.py
```
**Funcionalidades:**
- Sistema Q&A con modelo local (Ollama)
- Generación de FAQs
- Resumen ejecutivo
- Chatbot básico con OpenAI

#### Herramientas Individuales

#### Sistema de FAQs
- Generación automática de FAQs basadas en la base de conocimiento
- Exportación en formato texto
- Análisis de 25 fragmentos de contenido más relevantes

```bash
python llm/FAQ/faq_ollama.py
```

#### Generador de Resúmenes
- Resumen completo de información corporativa
- Análisis de historia, sostenibilidad, productos y logros
- Exportación en formato texto

```bash
python llm/summary/generate_summary.py
```

#### Sistema Q&A Básico
- Sistema de preguntas y respuestas usando modelos locales
- Preguntas predefinidas sobre Colombina
- Parámetros configurables (temperatura, top_p)

```bash
python llm/QA/qa_ollama.py
```

#### Web Scraping
```bash
python web_scraping/scripts/advanced_scraper.py
```

#### Procesamiento de Datos
```bash
# Limpiar archivos
python preprocessing/clean_md_files.py

# Preparar base de conocimiento
python knowledge_base/clean_kb.py

# Generar chunks
python chunking/chunking.py
```

---

## 📁 Arquitectura del Sistema

### Flujo de Datos - Primera Entrega
```
Web Scraping → Preprocessing → Knowledge Base → Chunking
     ↓
Análisis (FAQs, Q&A, Resúmenes) → Streamlit Interface (chatbot.py)
     ↓
Modelo Local (Ollama) sin vectorización → Respuestas Básicas
```

### Flujo de Datos - Segunda Entrega
```
Knowledge Base → Vector DB (ChromaDB) → RAG System
                      ↓
User Input → LangGraph Agent → Tools (RAG/Structured Data) → Response
                      ↓
                Memory Persistence → Streamlit Interface (app.py)
```

### Flujo de Datos - Tercera Entrega (Arquitectura Completa)
```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIOS / CLIENTES                      │
│  (Navegador Web, Apps Móviles, Integraciones API)           │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                  INTERFACES DE USUARIO                      │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐    │
│  │ HTML/CSS/JS  │  │  Streamlit   │  │   API REST      │    │
│  │  (Vanilla)   │  │  Interface   │  │  (FastAPI)      │    │
│  └──────┬───────┘  └──────┬───────┘  └────────┬────────┘    │
└─────────┼──────────────────┼───────────────────┼────────────┘
          │                  │                   │
          └──────────────────┴───────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE API (FastAPI)                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Endpoints: /chat, /health, /interface, /docs      │     │
│  │  Validación: Pydantic Models                        │    │
│  │  Seguridad: CORS, Environment Variables             │    │
│  └─────────────────────┬───────────────────────────────┘    │
└────────────────────────┼────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              AGENTE CONVERSACIONAL (LangGraph)              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • Memory Management (MemorySaver)                   │   │
│  │  • Session Tracking (thread_id)                      │   │
│  │  • Dynamic Parameters (temp, top_p, max_tokens)      │   │
│  │  • Fallback Logic                                    │   │
│  └────────────┬─────────────────────┬───────────────────┘   │
└───────────────┼─────────────────────┼───────────────────────┘
                ↓                     ↓
    ┌───────────────────┐ ┌───────────────────────┐
    │  Tool: RAG        │ │  Tool: Structured     │
    │  (ChromaDB)       │ │  Data (JSON)          │
    └─────────┬─────────┘ └─────────┬─────────────┘
              ↓                     ↓
┌─────────────────────────────────────────────────────────────┐
│                   FUENTES DE DATOS                          │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐    │
│  │  ChromaDB    │  │   JSON       │  │  Knowledge Base │    │
│  │  (Vectores)  │  │  (Datos)     │  │  (Documentos)   │    │
│  └──────────────┘  └──────────────┘  └─────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              SERVICIOS EXTERNOS / MONITOREO                 │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐    │
│  │   OpenAI     │  │  LangSmith   │  │    Railway      │    │
│  │  (GPT-4o)    │  │ (Tracing)    │  │  (Hosting)      │    │
│  └──────────────┘  └──────────────┘  └─────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Componentes Clave por Entrega

### Primera Entrega

#### [`web_scraping/scripts/advanced_scraper.py`](web_scraping/scripts/advanced_scraper.py)
Sistema robusto de extracción con categorización automática y manejo de errores.

#### [`utils/chunking/chunking.py`](utils/chunking/chunking.py)
División inteligente de contenido para optimización de consultas.

#### [`llm/summary/generate_summary.py`](llm/summary/generate_summary.py)
Análisis ejecutivo de información corporativa.

#### [`interface/streamlit/chatbot.py`](interface/streamlit/chatbot.py)
Interfaz Streamlit original con 4 pestañas: chatbot, Q&A, FAQs y resumen ejecutivo. Utiliza modelos locales sin vectorización.

### Segunda Entrega

#### [`RAG/agent/colombina_agent.py`](RAG/agent/colombina_agent.py)
Agente principal con LangGraph, memoria conversacional y orquestación de herramientas.

#### [`RAG/agent/tool_rag.py`](RAG/agent/tool_rag.py)
Herramienta RAG con ChromaDB y contextualización de consultas.

#### [`RAG/agent/tool_structured_data.py`](RAG/agent/tool_structured_data.py)
Acceso a datos fácticos específicos (contacto, horarios, NIT).

#### [`interface/streamlit/app.py`](interface/streamlit/app.py)
Interfaz Streamlit con gestión de sesiones y memoria persistente.

### Tercera Entrega

#### [`api/main.py`](api/main.py)
Aplicación FastAPI completa con:
- Endpoints REST (`/chat`, `/health`, `/interface`)
- Documentación automática (Swagger/ReDoc)
- Validación con Pydantic
- CORS configurado
- Modelos de request/response
- Manejo de errores
- Integración con el agente LangGraph

#### [`api_server.py`](api_server.py)
Servidor de producción optimizado:
- Configuración de puerto dinámico (Railway)
- Logging profesional
- Variables de entorno
- Ejecución con Uvicorn

#### [`interface/html/`](interface/html/)
Interfaz web moderna en HTML/CSS/JavaScript:
- **`index.html`**: Estructura del chat
- **`styles.css`**: Diseño moderno y responsivo
- **`app.js`**: Lógica del cliente y comunicación con API

#### Configuración de Despliegue

**`.env.example`**: Plantilla de configuración con:
- Variables obligatorias (OpenAI)
- Variables opcionales (LangSmith para trazabilidad)
- Documentación detallada

**`Procfile`**: Archivo de configuración de Railway que especifica el comando de inicio:
```
web: python api_server.py
```
Este archivo le indica a Railway cómo ejecutar la aplicación en producción.

**`railway.json`**: Configuración avanzada de Railway con:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python api_server.py",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```
Características:
- **Healthcheck automático**: Verifica `/health` cada cierto tiempo
- **Restart policy**: Reinicia automáticamente si falla
- **Timeout configurado**: 300 segundos para inicio
- **Builder optimizado**: Usa Nixpacks para detección automática de dependencias

**Railway Platform Configuration**:
- Detección automática de Python y dependencias
- Puerto asignado dinámicamente por Railway
- Variables de entorno configuradas en la plataforma
- Despliegue automático desde GitHub

---

## 📊 Métricas y Resultados

### Primera Entrega - Cobertura de Datos
- **294 URLs** extraídas del sitio oficial
- **130 chunks** optimizados generados
- **26 documentos** principales procesados
- **Sistema de logging** implementado

### Segunda Entrega - Funcionalidad Avanzada
- **Memoria conversacional** funcional
- **Sistema RAG** con búsqueda semántica
- **2 herramientas especializadas** integradas
- **Interfaz web** interactiva
- **Fallback inteligente** implementado

### Tercera Entrega - Producción y Escalabilidad
- **API REST** completamente funcional con 4+ endpoints
- **Despliegue en Railway** con 99.9% uptime
- **Trazabilidad LangSmith** con monitoreo en tiempo real
- **3 interfaces** diferentes (HTML, Streamlit x2)
- **Documentación automática** (Swagger + ReDoc)
- **Sistema de sesiones** robusto
- **Parámetros dinámicos** configurables por request
- **Healthcheck** para monitoreo de infraestructura

---

## 🧪 Evaluación y Testing

### Primera Entrega
```bash
# Evaluación en notebooks
jupyter lab tests/Taller1.ipynb
```

### Segunda Entrega
```bash
# Testing del agente
python RAG/agent/colombina_agent.py

# Testing de herramientas individuales
python RAG/agent/tool_rag.py
python RAG/agent/tool_structured_data.py
```

---

## 🔒 Mejores Prácticas Implementadas

### Todas las Entregas
- ✅ API Keys en variables de entorno
- ✅ Logging comprehensivo sin información sensible
- ✅ Manejo robusto de errores
- ✅ Separación clara entre datos y código
- ✅ Documentación técnica completa

### Segunda Entrega - Adicionales
- ✅ Gestión de estado con LangGraph
- ✅ Memory persistence entre sesiones
- ✅ Tool orchestration con fallback
- ✅ Interfaz de usuario intuitiva
- ✅ Arquitectura modular escalable

### Tercera Entrega - Producción
- ✅ API REST con FastAPI y validación Pydantic
- ✅ Documentación automática (OpenAPI/Swagger)
- ✅ CORS configurado para seguridad
- ✅ Healthchecks para monitoreo
- ✅ Despliegue automatizado en Railway
- ✅ Trazabilidad completa con LangSmith
- ✅ Variables de entorno seguras
- ✅ Múltiples interfaces para diferentes casos de uso
- ✅ Configuración de parámetros dinámicos
- ✅ Logging estructurado con emojis para mejor UX

---

## 🗺️ Roadmap de Desarrollo

### ✅ Primera Entrega (Completada)
- Infraestructura de datos
- Sistemas de análisis básico
- Pipeline de procesamiento
- Herramientas de extracción

### ✅ Segunda Entrega (Completada)
- Agente conversacional RAG
- Memoria persistente
- Interfaz web interactiva
- Sistema de herramientas

### ✅ Tercera Entrega (Completada)
- API REST con FastAPI
- Despliegue en Railway
- Trazabilidad con LangSmith
- Múltiples interfaces de usuario
- Sistema de monitoreo

---

## 👥 Contributors

### Equipo de Desarrollo

- **[Daniela Gómez Ayalde](https://github.com/DanielaGomez98)** - @DanielaGomez98
- **[Alejandro Arteaga](https://github.com/alejandroarteagaj)** - @alejandroarteagaj
- **[Juan Camilo Giraldo](https://github.com/Raldo26)** - @Raldo26
- **[Juan Felipe Hernández](https://github.com/Juanhernandez1972)** - @Juanhernandez1972

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Áreas de Contribución
- Mejora de prompts y modelos
- Nuevas fuentes de información
- Optimización de rendimiento
- Testing y validación
- Documentación y ejemplos
- Nuevas herramientas para el agente
- Mejoras en la API REST
- Nuevas interfaces de usuario
- Optimización de costos
- Seguridad y autenticación

---

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia Apache 2.0. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 📞 Contacto

Para preguntas o sugerencias sobre este centro de información, por favor contacta al equipo de desarrollo.

---

## 🔄 Changelog

### v3.0.0 - Tercera Entrega (2025-11-21) 🚀
- ✨ **NUEVO:** API REST completa con FastAPI
- ✨ **NUEVO:** Despliegue en Railway (producción 24/7)
- ✨ **NUEVO:** Trazabilidad con LangSmith
- ✨ **NUEVO:** Interfaz HTML/CSS/JS moderna
- ✨ **NUEVO:** Documentación automática (Swagger/ReDoc)
- ✨ **NUEVO:** Healthcheck endpoint
- ✨ **NUEVO:** Parámetros dinámicos del modelo (temperature, top_p, max_tokens)
- ✨ **NUEVO:** Sistema de sesiones robusto
- ✨ **NUEVO:** Variables de entorno con .env.example
- ✨ **NUEVO:** CORS configurado para múltiples clientes
- 🔧 **Mejorado:** Organización de interfaces en carpeta dedicada
- 🔧 **Mejorado:** Logging profesional con diagnósticos
- 🔧 **Mejorado:** Manejo de errores más granular
- 📚 **Documentación:** Guías de despliegue y configuración

### v2.0.0 - Segunda Entrega (2025-11-06)
- ✨ **NUEVO:** Agente conversacional con LangGraph
- ✨ **NUEVO:** Sistema RAG con ChromaDB
- ✨ **NUEVO:** Herramientas especializadas (RAG + datos estructurados)
- ✨ **NUEVO:** Memoria conversacional persistente
- ✨ **NUEVO:** Interfaz Streamlit interactiva
- ✨ **NUEVO:** Sistema de fallback inteligente
- � **Mejorado:** Logging con emojis y mejor trazabilidad

### v1.0.0 - Primera Entrega (2025-10-XX)
- 🎉 **Inicial:** Sistema de web scraping completo
- 🎉 **Inicial:** Pipeline de procesamiento de datos
- 🎉 **Inicial:** Generador de FAQs automático
- 🎉 **Inicial:** Sistema Q&A con Ollama (modelo local)
- 🎉 **Inicial:** Resumen ejecutivo automatizado
- 🎉 **Inicial:** Base de conocimiento estructurada
- 🎉 **Inicial:** Sistema de logging personalizado
- 🎉 **Inicial:** Interfaz Streamlit básica (chatbot.py) sin vectorización

---

**¡Explora el mundo de Colombina con inteligencia artificial! 🍭🤖**