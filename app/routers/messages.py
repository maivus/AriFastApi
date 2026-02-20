from fastapi import APIRouter, Request, Response, Query
from app.controllers.message_handler import process_message
from app.config import settings
from app.controllers.message_handler import handler # Importamos la instancia

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
    data = await request.json()
    
    # Extraer datos básicos para el handler
    entry = data.get("entry", [{}])[0]
    changes = entry.get("changes", [{}])[0]
    value = changes.get("value", {})
    contacts = value.get("contacts", [{}])[0]
    sender_name = contacts.get("profile", {}).get("name", "Usuario")
    messages = value.get("messages", [{}])

    if messages:
        await handler.handle_incoming_message(messages[0], sender_name)
    
    return {"status": "EVENT_RECEIVED"}