"""
Ejecuta el servidor FastAPI con Uvicorn.

Configuración:
    - Host: 0.0.0.0 (accesible desde cualquier IP)
    - Port: Variable de entorno PORT (default: 8000 para desarrollo)
    - Reload: False en producción

Usage:
    python api_server.py
    
O alternativamente:
    uvicorn api.main:app --host 0.0.0.0 --port $PORT
"""

import os
import uvicorn
from utils.logging_util.logger import get_logger

logger = get_logger()
    
if __name__ == "__main__":
    # Railway asigna el puerto dinámicamente mediante la variable PORT
    port = int(os.getenv("PORT", 8000))
    
    logger.info(f"🔧 Iniciando servidor FastAPI en puerto {port}...")
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )