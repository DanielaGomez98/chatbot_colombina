"""
FastAPI Application for Colombina RAG Chatbot

This API exposes the Colombina conversational agent with RAG capabilities.
It provides endpoints for chat interactions with persistent memory across sessions.

Author: Equipo Colombina
Version: 2.0.0
"""

import os
import sys
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.logging_util.logger import get_logger
from RAG.agent.colombina_agent import app as agent_app

logger = get_logger()


# ========== Lifespan Event Handler ==========

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manejador de eventos del ciclo de vida de la aplicación.
    
    Startup: Se ejecuta al iniciar la aplicación
    Shutdown: Se ejecuta al cerrar la aplicación
    """
    # Startup
    logger.info("🚀 Iniciando Colombina RAG Chatbot API v2.0.0")
    logger.info("📚 Agente conversacional cargado")
    logger.info("🔗 Documentación disponible en /docs")
    
    yield
    
    # Shutdown
    logger.info("🛑 Cerrando Colombina RAG Chatbot API")


# Initialize FastAPI app
app = FastAPI(
    title="Colombina RAG Chatbot API",
    description="API REST para el agente conversacional de Colombina con RAG y memoria persistente",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== Request/Response Models ==========

class ChatRequest(BaseModel):
    """
    Modelo de solicitud para el endpoint de chat.
    
    Attributes:
        message (str): Mensaje del usuario para el chatbot
        session_id (str): Identificador único de la sesión de conversación
    
    Examples:
        {
            "message": "¿Cuál es la misión de Colombina?",
            "session_id": "user-123-session-abc"
        }
    """
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Mensaje del usuario (1-2000 caracteres)",
        example="¿Cuál es el NIT de la empresa?"
    )
    session_id: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="ID único de sesión para mantener el contexto conversacional",
        example="user-123-session-456"
    )


class ChatResponse(BaseModel):
    """
    Modelo de respuesta del endpoint de chat.
    
    Attributes:
        response (str): Respuesta generada por el agente
        session_id (str): ID de sesión usado en la conversación
        success (bool): Indica si la operación fue exitosa
    
    Examples:
        {
            "response": "El NIT de Colombina es 890.301.244-4",
            "session_id": "user-123-session-abc",
            "success": true
        }
    """
    response: str = Field(
        ...,
        description="Respuesta del agente conversacional"
    )
    session_id: str = Field(
        ...,
        description="ID de sesión utilizado"
    )
    success: bool = Field(
        default=True,
        description="Estado de la operación"
    )


class ErrorResponse(BaseModel):
    """
    Modelo de respuesta para errores.
    
    Attributes:
        detail (str): Descripción del error
        session_id (Optional[str]): ID de sesión si está disponible
        success (bool): Siempre False para errores
    """
    detail: str = Field(
        ...,
        description="Descripción del error"
    )
    session_id: Optional[str] = Field(
        None,
        description="ID de sesión si está disponible"
    )
    success: bool = Field(
        default=False,
        description="Estado de la operación (siempre False para errores)"
    )


class HealthResponse(BaseModel):
    """
    Modelo de respuesta para el endpoint de salud.
    
    Attributes:
        status (str): Estado del servicio
        version (str): Versión de la API
    """
    status: str = Field(
        default="healthy",
        description="Estado del servicio"
    )
    version: str = Field(
        default="2.0.0",
        description="Versión de la API"
    )


# ========== Endpoints ==========

@app.get(
    "/",
    tags=["General"],
    summary="Endpoint raíz",
    description="Retorna información básica de la API"
)
async def root():
    """
    Endpoint raíz de la API.
    
    Returns:
        dict: Información básica de la API
    """
    return {
        "name": "Colombina RAG Chatbot API",
        "version": "2.0.0",
        "description": "API para interactuar con el agente conversacional de Colombina",
        "docs": "/docs",
        "health": "/health"
    }


@app.get(
    "/health",
    tags=["General"],
    response_model=HealthResponse,
    summary="Verificación de salud",
    description="Verifica que el servicio esté funcionando correctamente"
)
async def health_check():
    """
    Endpoint para verificar el estado de salud del servicio.
    
    Returns:
        HealthResponse: Estado y versión del servicio
    
    Raises:
        HTTPException: Si el servicio no está disponible
    """
    try:
        logger.info("🏥 Health check solicitado")
        return HealthResponse(status="healthy", version="2.0.0")
    except Exception as e:
        logger.error(f"❌ Error en health check: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unavailable"
        )


@app.post(
    "/chat",
    tags=["Chat"],
    response_model=ChatResponse,
    responses={
        200: {
            "description": "Respuesta exitosa del chatbot",
            "model": ChatResponse
        },
        400: {
            "description": "Solicitud inválida",
            "model": ErrorResponse
        },
        500: {
            "description": "Error interno del servidor",
            "model": ErrorResponse
        }
    },
    summary="Enviar mensaje al chatbot",
    description="""
    Envía un mensaje al agente conversacional de Colombina y recibe una respuesta.
    
    El agente utiliza:
    - **RAG (Retrieval-Augmented Generation)**: Para consultas complejas sobre la empresa
    - **Datos estructurados**: Para información específica (NIT, contactos, etc.)
    - **Memoria conversacional**: Mantiene el contexto entre mensajes de la misma sesión
    - **Sistema de fallback**: Intenta múltiples estrategias para encontrar respuestas
    
    **Importante**: Use el mismo `session_id` para mantener el contexto conversacional.
    """
)
async def chat(request: ChatRequest):
    """
    Procesa un mensaje del usuario y retorna la respuesta del agente.
    
    Args:
        request (ChatRequest): Solicitud con el mensaje del usuario y session_id
    
    Returns:
        ChatResponse: Respuesta del agente conversacional
    
    Raises:
        HTTPException: 
            - 400: Si los parámetros son inválidos
            - 500: Si ocurre un error al procesar el mensaje
    
    Example:
        ```python
        import requests
        
        response = requests.post(
            "http://localhost:8000/chat",
            json={
                "message": "¿Cuál es la misión de Colombina?",
                "session_id": "user-123-session-456"
            }
        )
        print(response.json())
        # {
        #     "response": "La misión de Colombina es...",
        #     "session_id": "user-123-session-456",
        #     "success": true
        # }
        ```
    """
    try:
        logger.info(f"💬 Nuevo mensaje - Session: {request.session_id}")
        logger.info(f"👤 Mensaje del usuario: {request.message}")
        
        if not request.message.strip():
            logger.warning("⚠️ Mensaje vacío recibido")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El mensaje no puede estar vacío"
            )
        
        if not request.session_id.strip():
            logger.warning("⚠️ Session ID vacío recibido")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El session_id no puede estar vacío"
            )
        
        config = {"configurable": {"thread_id": request.session_id}}

        input_message = {"type": "human", "content": request.message}

        logger.info("🤖 Invocando agente conversacional...")
        final_state = agent_app.invoke(
            {"messages": [input_message]},
            config=config
        )

        final_response_dict = final_state['messages'][-1]
        response_content = final_response_dict.get(
            'content', 
            'Lo siento, no pude generar una respuesta.'
        )
        
        logger.info(f"✅ Respuesta generada exitosamente")
        logger.info(f"🤖 Respuesta: {response_content[:100]}...")
        
        return ChatResponse(
            response=response_content,
            session_id=request.session_id,
            success=True
        )
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"❌ Error procesando mensaje: {str(e)}")
        logger.error(f"📋 Detalles: {type(e).__name__}")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar el mensaje: {str(e)}"
        )