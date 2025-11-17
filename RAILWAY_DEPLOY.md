# ============================================
# GUÍA DE DESPLIEGUE EN RAILWAY
# ============================================

## 📦 Archivos creados para el despliegue:

1. **Procfile**: Indica a Railway cómo ejecutar la aplicación
2. **railway.json**: Configuración específica de Railway (healthcheck, restart policy)
3. **.env.example**: Plantilla de variables de entorno necesarias
4. **requirements.txt**: Dependencias de Python (formato corregido)
5. **api_server.py**: Modificado para usar puerto dinámico de Railway

## 🚀 Pasos para desplegar en Railway:

### 1. Preparar el repositorio
```bash
# Asegúrate de que todos los cambios estén en Git
git add .
git commit -m "Configuración para Railway"
git push origin main
```

### 2. En Railway (railway.app)

#### A. Crear nuevo proyecto
1. Ve a https://railway.app
2. Click en "New Project"
3. Selecciona "Deploy from GitHub repo"
4. Autoriza Railway a acceder a tus repositorios
5. Selecciona el repositorio `chatbot_colombina`

#### B. Configurar variables de entorno
1. Ve a la pestaña "Variables"
2. Click en "New Variable"
3. Agrega las siguientes variables:

```
OPENAI_API_KEY=tu_api_key_real_aqui
```

**IMPORTANTE:** No configures `PORT` - Railway lo asigna automáticamente.

#### C. Configurar el servicio
Railway detectará automáticamente:
- Python como lenguaje
- `requirements.txt` para instalar dependencias
- `Procfile` para el comando de inicio

#### D. Desplegar
1. Railway iniciará el despliegue automáticamente
2. Espera a que termine (verás logs en tiempo real)
3. Una vez completado, obtendrás una URL pública

### 3. Verificar el despliegue

Una vez desplegado, puedes verificar que funciona:

```bash
# Reemplaza <tu-url> con la URL que te dio Railway
curl https://<tu-url>.railway.app/health

# Debería retornar:
# {"status":"healthy","version":"2.0.0"}
```

### 4. Probar la API

```bash
# Endpoint de prueba
curl -X POST https://<tu-url>.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Cuál es el NIT de Colombina?",
    "session_id": "test-123"
  }'
```

### 5. Acceder a la interfaz web

Abre en tu navegador:
```
https://<tu-url>.railway.app/interface
```

## 🔧 Configuración adicional (opcional)

### Configurar dominio personalizado
1. En Railway, ve a "Settings"
2. Sección "Domains"
3. Click "Generate Domain" o "Custom Domain"

### Ver logs en tiempo real
1. En Railway, pestaña "Deployments"
2. Click en el despliegue activo
3. Verás los logs en tiempo real

### Reiniciar el servicio
1. Ve a "Deployments"
2. Click en "..." (tres puntos)
3. "Restart"

## ⚠️ Notas importantes

1. **Base de datos Chroma**: Actualmente usas ChromaDB local (`RAG/chroma_db/`). En Railway, los datos persistirán SOLO si montas un volumen. Si no lo haces, se perderán en cada despliegue.

2. **Volumen persistente** (para mantener ChromaDB):
   - En Railway, ve a "Volumes"
   - Click "New Volume"
   - Mount path: `/app/RAG/chroma_db`
   - Size: Según necesites (ej: 1GB)

3. **Costos**: Railway tiene un tier gratuito con $5 de crédito mensual. Monitorea tu uso.

4. **Timeout**: Railway tiene un timeout de 300 segundos (5 minutos) para healthchecks. Si tu app tarda más en iniciar, ajusta en `railway.json`.

## 🐛 Troubleshooting

### El servicio no inicia
- Revisa los logs en Railway
- Verifica que `OPENAI_API_KEY` esté configurada
- Asegúrate que todos los archivos estén en Git

### Error de puerto
- No configures `PORT` manualmente
- Railway lo asigna automáticamente

### Dependencias faltantes
- Verifica que `requirements.txt` tenga todas las dependencias
- Sin comas al final de cada línea

### ChromaDB se pierde
- Configura un volumen persistente (ver arriba)

## 📚 Recursos útiles

- Documentación Railway: https://docs.railway.app
- Dashboard Railway: https://railway.app/dashboard
- Logs: https://railway.app/project/<tu-proyecto>/deployments

## 🎯 Endpoints disponibles

Una vez desplegado:
- `GET /` - Info de la API
- `GET /health` - Healthcheck
- `GET /interface` - Interfaz web
- `POST /chat` - Endpoint principal del chatbot
- `GET /docs` - Documentación Swagger
- `GET /redoc` - Documentación ReDoc
