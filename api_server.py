"""
Ejecuta el servidor FastAPI con Uvicorn.

Configuración:
    - Host: 0.0.0.0 (accesible desde cualquier IP)
    - Port: 8000
    - Reload: True (recarga automática en desarrollo)

Usage:
    python api/main.py
    
O alternativamente:
    uvicorn api.main:app --reload
"""

import uvicorn
from utils.logging_util.logger import get_logger

logger = get_logger()
    
logger.info("🔧 Iniciando servidor FastAPI...")

uvicorn.run(
    "api.main:app",
    host="0.0.0.0",
    port=8000,
    reload=True,
    log_level="info"
)