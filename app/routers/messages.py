from fastapi import APIRouter, Request, Response, Query
import logging

# Configuramos logs para ver qué llega en Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["WhatsApp Webhook"])

@router.get("/")
async def verify_webhook(
    token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge")
):
    # Este es el token que pondrás en el panel de Meta
    VERIFY_TOKEN = "ari_token_2026" 
    
    if token == VERIFY_TOKEN:
        logger.info("Webhook verificado con éxito")
        return Response(content=challenge, media_type="text/plain")
    
    return Response(content="Error de token", status_code=403)

@router.post("/")
async def receive_messages(request: Request):
    data = await request.json()
    logger.info(f"Datos recibidos: {data}")
    
    # Aquí es donde la estructura MVC entra en juego
    # Próximamente: message_handler.process(data)
    
    return {"status": "EVENT_RECEIVED"}