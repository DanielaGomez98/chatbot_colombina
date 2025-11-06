import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

load_dotenv()

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from logging_util.logger import get_logger

logger = get_logger()

chunks_path = project_root / "chunking" / "chunks.json"
db_directory = project_root / "RAG" / "chroma_db"
logger.info(f"📂 Cargando chunks desde: {chunks_path}")


API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    logger.error("❌ API Key de OpenAI no encontrada en variables de entorno")
    raise ValueError("OPENAI_API_KEY no configurada")


try:
    with open(chunks_path, 'rb') as f:
        raw_bytes = f.read()
        
        try:
            json_string = raw_bytes.decode('utf-8')
        except UnicodeDecodeError:
            json_string = raw_bytes.decode('windows-1252', errors='replace')
        
        data = json.loads(json_string) 

except Exception as e:
    logger.error(f"❌ Error al leer archivo de chunks: {e}")
    sys.exit(1)


documents = []
for item in data:
    safe_content = item['content'].encode('utf-8', 'ignore').decode('utf-8')
    
    documents.append(
        Document(
            page_content=safe_content,
            metadata=item['metadata']
        )
    )


try:
    logger.info("🔧 Creando base de datos vectorial...")
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(api_key=API_KEY), 
        persist_directory=str(db_directory)
    )
    logger.info("✅ Base de datos vectorial creada exitosamente")
    
except Exception as e:
    logger.error(f"❌ Error al crear base de datos vectorial: {e}")
    sys.exit(1)