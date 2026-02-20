from fastapi import APIRouter, Query, Response

router = APIRouter(prefix="/webhook", tags=["WhatsApp Webhook"])

@router.get("/")
async def verify_webhook(
    token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge")
):
    # Asegúrate de que este TOKEN sea el MISMO que escribes en Meta
    VERIFY_TOKEN = "ari_token_2026" 
    
    if token == VERIFY_TOKEN:
        # IMPORTANTE: Devolver el challenge directamente como texto
        return Response(content=str(challenge), media_type="text/plain")
    
    return Response(content="Token incorrecto", status_code=403)