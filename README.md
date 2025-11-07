# 🍭 Centro de Información Colombina

Un sistema integral de inteligencia artificial especializado en **Colombina**, desarrollado en dos entregas que evolucionaron desde un chatbot básico hasta un agente conversacional avanzado con múltiples herramientas de IA.

## 📋 Evolución del Proyecto

### 📦 Primera Entrega: Fundación del Sistema
**Objetivo:** Crear la infraestructura base de datos y análisis de información corporativa

### 📦 Segunda Entrega: Agente Conversacional Avanzado  
**Objetivo:** Implementar un sistema RAG completo con memoria conversacional y herramientas especializadas

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
├── web_scraping/              # Sistema de extracción web
├── preprocessing/             # Procesamiento de datos
├── chunking/                  # División de contenido
├── knowledge_base/            # Base de conocimiento
├── llm/                       # Módulos de IA básicos
│   ├── FAQ/                   # Generador de FAQs
│   ├── QA/                    # Sistema Q&A básico
│   └── summary/               # Generador de resúmenes
├── logging_util/              # Sistema de logging
└── chatbot.py                 # Interfaz Streamlit básica (4 pestañas)
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
├── RAG/                       # 🆕 Sistema RAG completo
│   ├── agent/                 # Agente conversacional
│   │   ├── colombina_agent.py # Agente principal LangGraph
│   │   ├── tool_rag.py        # Herramienta RAG
│   │   └── tool_structured_data.py # Herramienta datos estructurados
│   ├── vector_db/             # Base de datos vectorial
│   │   └── load_data.py       # Carga de embeddings
│   └── chroma_db/             # ChromaDB persistente
└── app.py                     # 🆕 Interfaz Streamlit
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

---

## 🔧 Instalación y Configuración

### Requisitos Previos
- Python 3.13 o superior
- API Key de OpenAI
- Ollama instalado (para funciones de primera entrega)
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
echo "OPENAI_API_KEY=tu_api_key_aqui" > .env

# Instalar Ollama (opcional, para primera entrega)
ollama pull gpt-oss:20b
```

---

## 🏃‍♂️ Uso del Sistema

### 🎯 Agente Conversacional (Segunda Entrega)
```bash
# Interfaz principal Streamlit con agente RAG
streamlit run app.py
```
**Funcionalidades:**
- Conversación natural con memoria persistente
- Consultas sobre Colombina usando RAG
- Datos estructurados (contacto, horarios, NIT)
- Sistema de fallback inteligente

### 📊 Interfaz Básica y Herramientas de Análisis (Primera Entrega)

#### Interfaz Streamlit Original
```bash
# Interfaz básica con 4 pestañas (modelo local sin RAG)
streamlit run chatbot.py
```
**Funcionalidades:**
- Sistema Q&A con modelo local (Ollama)
- Generación de FAQs
- Resumen ejecutivo
- Chatbot básico con OpenAI

#### Herramientas Individuales

#### Sistema de FAQs
```bash
python llm/FAQ/faq_ollama.py
```

#### Generador de Resúmenes
```bash
python llm/summary/generate_summary.py
```

#### Sistema Q&A Básico
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

# Generar chunks
python chunking/chunking.py

# Preparar base de conocimiento
python knowledge_base/clean_kb.py
```

---

## 📁 Arquitectura del Sistema

### Flujo de Datos - Primera Entrega
```
Web Scraping → Preprocessing → Chunking → Knowledge Base
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

---

## � Componentes Clave por Entrega

### Primera Entrega

#### [`web_scraping/scripts/advanced_scraper.py`](web_scraping/scripts/advanced_scraper.py)
Sistema robusto de extracción con categorización automática y manejo de errores.

#### [`chunking/chunking.py`](chunking/chunking.py)
División inteligente de contenido para optimización de consultas.

#### [`llm/summary/generate_summary.py`](llm/summary/generate_summary.py)
Análisis ejecutivo de información corporativa.

#### [`chatbot.py`](chatbot.py)
Interfaz Streamlit original con 4 pestañas: chatbot, Q&A, FAQs y resumen ejecutivo. Utiliza modelos locales sin vectorización.

### Segunda Entrega

#### [`RAG/agent/colombina_agent.py`](RAG/agent/colombina_agent.py)
Agente principal con LangGraph, memoria conversacional y orquestación de herramientas.

#### [`RAG/agent/tool_rag.py`](RAG/agent/tool_rag.py)
Herramienta RAG con ChromaDB y contextualización de consultas.

#### [`RAG/agent/tool_structured_data.py`](RAG/agent/tool_structured_data.py)
Acceso a datos fácticos específicos (contacto, horarios, NIT).

#### [`app.py`](app.py)
Interfaz Streamlit con gestión de sesiones y memoria persistente.

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

### Ambas Entregas
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

---

## � Roadmap de Desarrollo

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

---

## 👥 Contributors

### Equipo de Desarrollo

- **[Daniela Gómez Ayalde](https://github.com/DanielaGomez98)** - @DanielaGomez98
- **[Nombre Desarrollador 2](https://github.com/usuario2)** - @usuario2  
- **[Nombre Desarrollador 3](https://github.com/usuario3)** - @usuario3
- **[Nombre Desarrollador 4](https://github.com/usuario4)** - @usuario4

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

---

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia Apache 2.0. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 🔄 Changelog

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

**¡Explora el mundo de Colombina con inteligencia artificial avanzada! 🍭🤖**

## 🚀 Tecnologías Utilizadas

### Backend y IA
- **Python 3.13+**
- **LangChain** - Framework para LLMs y RAG
- **OpenAI GPT-4o** - Modelo principal para el chatbot
- **Ollama** - Modelos locales (gpt-oss:20b)
- **Streamlit** - Interfaz web multi-tab

### Web Scraping y Procesamiento
- **Selenium** - Automatización web avanzada
- **BeautifulSoup4** - Parsing HTML
- **PyPDF2** - Extracción de contenido PDF
- **RecursiveCharacterTextSplitter** - Chunking inteligente

### Almacenamiento y Logging
- **JSON** - Base de conocimiento estructurada
- **CSV** - Exportación de datos
- **Logging personalizado** - Sistema de trazabilidad

## 📋 Requisitos Previos

- Python 3.13 o superior
- API Key de OpenAI
- Ollama instalado (para funciones Q&A y FAQ)
- Chrome/Chromium (para web scraping)
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
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
uv pip install -r pyproject.toml
```

3. **Configurar variables de entorno**
```bash
# Crear archivo .env en la raíz del proyecto
echo "OPENAI_API_KEY=tu_api_key_aqui" > .env
```

4. **Instalar Ollama (opcional, para Q&A local)**
```bash
# Instalar Ollama desde https://ollama.ai
ollama pull gpt-oss:20b
```

## 🏃‍♂️ Uso

### Interfaz Principal (Streamlit)
```bash
streamlit run chatbot.py
```

La aplicación incluye 4 pestañas principales:

#### 🔍 **Consulta Q&A**
- Sistema de preguntas y respuestas usando modelos locales
- Preguntas predefinidas sobre Colombina
- Parámetros configurables (temperatura, top_p)

#### ❓ **Preguntas Frecuentes** 
- Generación automática de FAQs basadas en la base de conocimiento
- Exportación en formato texto
- Análisis de 25 fragmentos de contenido más relevantes

#### 📋 **Resumen Ejecutivo**
- Resumen completo de información corporativa
- Análisis de historia, sostenibilidad, productos y logros
- Exportación en formato texto

#### 💬 **Chatbot Interactivo**
- Conversación natural con GPT-4o
- Memoria de conversación por sesión
- Respuestas especializadas en Colombina

### Funciones Individuales

#### Web Scraping
```bash
# Extracción básica de links
python web_scraping/scripts/extract_colombina_links.py

# Scraping avanzado con contenido completo
python web_scraping/scripts/advanced_scraper.py
```

#### Procesamiento de Datos
```bash
# Limpiar archivos markdown y crear la base de conocimiento
python preprocessing/clean_md_files.py

# Limpiar base de conocimiento
python knowledge_base/clean_kb.py

# Generar chunks
python chunking/chunking.py
```

#### Sistemas de IA Individuales
```bash
# Generar FAQs
python llm/FAQ/faq_ollama.py

# Sistema Q&A
python llm/QA/qa_ollama.py

# Generar resumen
python llm/summary/generate_summary.py
```

## 📁 Estructura del Proyecto

```
chatbot_colombina/
├── chatbot.py                     # 🎯 Interfaz principal Streamlit
├── requirements.txt               # 📦 Dependencias del proyecto
├── pyproject.toml                # ⚙️ Configuración del proyecto
├── 
├── llm/                          # 🤖 Módulos de IA
│   ├── llm_openai.py            # OpenAI GPT-4o integration
│   ├── FAQ/
│   │   └── faq_openai.py        # Generador de FAQs
│   ├── QA/
│   │   └── qa_ollama.py         # Sistema Q&A con Ollama
│   └── summary/
│       └── generate_summary.py  # Generador de resúmenes
│
├── web_scraping/                 # 🕷️ Sistema de scraping
│   ├── scripts/
│   │   ├── extract_colombina_links.py
│   │   └── advanced_scraper.py   # Scraper principal
│   ├── colombina_advanced/       # Datos extraídos
│   │   └── data/
│   │       ├── noticias/
│   │       └── otros/
│   └── pdf_extraction/           # PDFs procesados
│       └── markdown/
│
├── preprocessing/                # 🔄 Procesamiento de datos
│   ├── clean_md_files.py        # Limpieza de markdown
│   ├── selected_md_files/       # Archivos seleccionados
│   └── cleaned_md_files/        # Archivos procesados
│
├── chunking/                     # ✂️ División de contenido
│   ├── chunking.py              # Generación de chunks
│   └── chunks.json              # Chunks para RAG
│
├── knowledge_base/              # 📚 Base de conocimiento
│   ├── knowledge_base.txt       # Base original
│   ├── improved_knowledge_base.txt # Base mejorada
│   └── clean_kb.py             # Script de limpieza
│
├── logging_util/               # 📊 Sistema de logging
│   ├── logger.py              # Configuración de logs
│   └── logs/                  # Archivos de log
│
└── tests/                     # 🧪 Pruebas y análisis
    └── Taller1.ipynb         # Notebooks de evaluación
```

## ⚙️ Configuración Avanzada

### Parámetros del Modelo

#### Chatbot Interactivo (GPT-4o)
- **🌡️ Temperatura (0.0-1.0)**: Creatividad de respuestas (default: 0.1)
- **🎯 Top P (0.0-1.0)**: Diversidad de vocabulario (default: 0.9)

#### Sistema Q&A (Ollama)
- **Modelo**: gpt-oss:20b (configurable)
- **Chunks máximos**: 25 fragmentos por consulta
- **Tamaño de chunk**: 1000 caracteres con overlap de 200

#### Web Scraping
- **Categorías**: noticias, productos, sostenibilidad, otros
- **Formato de salida**: Markdown enriquecido con metadatos
- **Límite de URLs**: Configurable (294 URLs totales detectadas)

### Sistema de Logging
```python
# Configuración en logging_util/logger.py
- Rotación automática de archivos
- Niveles: DEBUG, INFO, WARNING, ERROR
- Formato timestamped con colores
- Archivos separados por módulo
```

## 💬 Ejemplos de Uso

### Preguntas de Ejemplo para Q&A
- "¿Cómo se llama el programa de Colombina para acompañar a sus proveedores y emprendedores?"
- "¿Qué porcentaje de la energía eléctrica que utiliza Colombina en Colombia proviene de fuentes renovables?"
- "¿Cuáles son los principales logros de Colombina en materia de sostenibilidad relacionados con la energía y el agua?"
- "¿Cuándo y cómo fue fundada Colombina?"
- "¿En cuántos países tiene presencia la empresa actualmente?"

### Consultas para el Chatbot
- "¿Qué productos fabrica Colombina?"
- "Cuéntame sobre la historia de Bon Bon Bum"
- "¿Qué ingredientes tienen los chocolates Nucita?"
- "¿Dónde puedo comprar productos Colombina?"
- "¿Cuáles son las iniciativas de sostenibilidad de la empresa?"

## 🔍 Base de Conocimiento

### Fuentes de Información
- **Sitio Web Oficial**: 294 URLs categorizadas y procesadas
- **Informes Anuales**: PDFs extraídos y convertidos a texto
- **Documentos Corporativos**: Códigos de conducta, políticas
- **Noticias**: Lanzamientos, colaboraciones, logros

### Cobertura Temática
- **📈 Historia y Expansión**: Fundación, crecimiento, internacionalización
- **🌱 Sostenibilidad**: Energía renovable, gestión de residuos, huella de carbono
- **🍬 Productos**: Catálogo completo, marcas, innovaciones
- **👥 Responsabilidad Social**: Programas comunitarios, equidad de género
- **💼 Información Corporativa**: Gobierno, finanzas, certificaciones
- **📞 Contacto**: Proveedores, servicio al cliente, sedes

## 🛠️ Desarrollo y Arquitectura

### Flujo de Datos
1. **Extracción**: [`advanced_scraper.py`](web_scraping/scripts/advanced_scraper.py) → sitio web
2. **Procesamiento**: [`clean_md_files.py`](preprocessing/clean_md_files.py) → archivos limpios
3. **Chunking**: [`chunking.py`](chunking/chunking.py) → fragmentos para RAG
4. **IA**: Modelos locales (Ollama) y remotos (OpenAI)

### Componentes Clave

#### [`chatbot.py`](chatbot.py)
Interfaz principal con 4 tabs especializados, configuración de parámetros y manejo de estado.

#### [`llm/llm_openai.py`](llm/llm_openai.py)
Core del chatbot con prompt especializado y manejo de errores.

#### [`web_scraping/scripts/advanced_scraper.py`](web_scraping/scripts/advanced_scraper.py)
Scraper robusto con categorización automática y manejo de errores.

#### [`chunking/chunking.py`](chunking/chunking.py)
Sistema de división inteligente de contenido para optimizar el RAG.

### Agregar Nuevas Funcionalidades

1. **Modificar prompts**: Editar templates en módulos LLM
2. **Agregar fuentes**: Extender el scraper o agregar procesadores
3. **Nuevos modelos**: Integrar en [`llm/`](llm/) con configuración similar
4. **Mejorar chunking**: Ajustar parámetros en [`chunking.py`](chunking/chunking.py)
5. **Extend UI**: Agregar tabs en [`chatbot.py`](chatbot.py)

## 📊 Métricas y Evaluación

### Cobertura de Información
- **294 URLs** procesadas del sitio oficial
- **130 chunks** generados para RAG
- **26 documentos** principales procesados
- **Multiple PDFs** de informes anuales integrados

### Rendimiento del Sistema
- **Tiempo de respuesta Q&A**: ~1-2 minutos (modelo local)
- **Tiempo de respuesta Chatbot**: ~5-10 segundos (OpenAI)
- **Precisión evaluada**: Sistema de evaluación en [`tests/Taller1.ipynb`](tests/Taller1.ipynb)

## 🔒 Seguridad y Mejores Prácticas

- ✅ API Keys en variables de entorno
- ✅ Logs sin información sensible
- ✅ Validación de entrada en todos los módulos
- ✅ Manejo robusto de errores y excepciones
- ✅ Separación clara entre datos y código
- ✅ Licencia Apache 2.0 para uso comercial

## 🐛 Solución de Problemas

### Errores Comunes

#### "Falta la API Key de OpenAI"
```bash
# Verificar archivo .env
cat .env
# Debe contener: OPENAI_API_KEY=sk-...
```

#### "Ollama model not found"
```bash
# Instalar modelo requerido
ollama pull gpt-oss:20b
```

#### Error en Web Scraping
```bash
# Verificar Chrome/Chromium instalado
# Revisar logs en logging_util/logs/
```

#### Chunks no generados
```bash
# Verificar base de conocimiento
python chunking/chunking.py
# Revisar knowledge_base/improved_knowledge_base.txt
```

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia Apache 2.0. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🚧 Estado del Proyecto

**Versión actual: 1.0.0**

### Completado ✅
- Sistema completo de web scraping
- Pipeline de procesamiento de datos
- 4 interfaces de IA especializadas
- Base de conocimiento integral
- Sistema de logging avanzado
- Evaluación y métricas
- Documentación completa

### Futuras Mejoras 🚀
- Integración con bases de datos vectoriales
- API REST para integración externa
- Sistema de caché para optimizar rendimiento
- Interfaz administrativa para gestión de contenido

## 👥 Contributors

### Equipo de Desarrollo

- **[Daniela Gómez Ayalde](https://github.com/DanielaGomez98)** - @DanielaGomez98
- **[Alejandro Arteaga](https://github.com/alejandroarteagaj)** - @alejandroarteagaj
- **[Juan Camilo Giraldo](https://github.com/Raldo26)** - @Raldo26
- **[Juan Felipe Hernández](https://github.com/Juanhernandez1972)** - @Juanhernandez1972

### Metodología de Trabajo

- **Code Review**: Revisión cruzada de código entre miembros del equipo
- **Documentación Compartida**: Mantenimiento colaborativo de documentación técnica

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

## 📞 Contacto

Para preguntas o sugerencias sobre este centro de información, por favor contacta al equipo de desarrollo.

---

**¡Explora el mundo de Colombina con inteligencia artificial! 🍭**