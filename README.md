# 🍭 Centro de Información Colombina

Un sistema integral de inteligencia artificial especializado en **Colombina**, la empresa líder en dulces y confitería de Colombia y Latinoamérica. Este centro combina web scraping, procesamiento de documentos, análisis de contenido y múltiples interfaces de IA para brindar información completa sobre la empresa.

## 🌟 Características Principales

- **💬 Chatbot Interactivo**: Conversación natural usando OpenAI GPT-4o
- **🔍 Sistema Q&A**: Consultas específicas con modelos locales (Ollama)
- **❓ Generador de FAQs**: Creación automática de preguntas frecuentes
- **📋 Resumen Ejecutivo**: Análisis integral de información corporativa
- **🕷️ Web Scraping Avanzado**: Extracción automática del sitio oficial de Colombina
- **📄 Procesamiento de PDFs**: Extracción de informes anuales y documentos corporativos
- **🔄 Pipeline de Chunking**: División inteligente de contenido para RAG
- **📊 Logging Avanzado**: Sistema completo de trazabilidad y monitoreo

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