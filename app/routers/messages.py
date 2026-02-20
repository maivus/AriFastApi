from fastapi import APIRouter, Request, Response, Query
from app.controllers.message_handler import handler
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
        
        # Extraer datos básicos para enviarlos al handler
        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        
        # Extraer el nombre del perfil
        contacts = value.get("contacts", [{}])
        sender_name = contacts[0].get("profile", {}).get("name", "Usuario") if contacts else "Usuario"
        
        messages = value.get("messages", [{}])

        if messages:
            # Ahora llamamos a handler.handle_incoming_message
            await handler.handle_incoming_message(messages[0], sender_name)
        
        return {"status": "EVENT_RECEIVED"}
    
    except Exception as e:
        print(f"Error en router: {e}")
        return {"status": "error", "message": str(e)}