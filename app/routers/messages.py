from fastapi import APIRouter, Request, Response, Query
from app.controllers.message_handler import process_message
from app.config import settings

# Configuramos el router
router = APIRouter(prefix="/webhook", tags=["WhatsApp Webhook"])

# --- VERIFICACIÓN DEL WEBHOOK (GET) ---
# Usamos dos rutas para capturar /webhook y /webhook/
@router.get("")
@router.get("/")
async def verify_webhook(
    token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge")
):
    # El token que configuraste en el panel de Meta
    VERIFY_TOKEN = "ari_token_2026" 
    
    if token == settings.VERIFY_TOKEN:
        # Es vital devolver el challenge como texto plano para Meta
        return Response(content=str(challenge), media_type="text/plain")
    
    return Response(content="Token de verificación inválido", status_code=403)


# --- RECEPCIÓN DE MENSAJERÍA (POST) ---
# Usamos dos rutas para evitar el error 307 de redirección
@router.post("")
@router.post("/")
async def receive_messages(request: Request):
    try:
        data = await request.json()
        
        # Enviamos la data a nuestro controlador (lógica de Ari)
        await process_message(data)
        
        return {"status": "EVENT_RECEIVED"}
    
    except Exception as e:
        # Si algo falla en la lectura del JSON, devolvemos un 200 para que Meta 
        # no reintente infinitamente el envío
        return {"status": "error", "message": str(e)}