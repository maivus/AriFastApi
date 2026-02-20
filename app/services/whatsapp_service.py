import httpx
from app.config import settings

async def send_whatsapp_request(payload: dict):
    """Función base para evitar repetir código de headers y URL"""
    url = f"https://graph.facebook.com/v18.0/{settings.PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            return response.json()
        except Exception as e:
            print(f"Error en la API de WhatsApp: {e}")
            return None

async def send_message(to: str, text: str, message_id: str = None):
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    if message_id:
        payload["context"] = {"message_id": message_id}
    return await send_whatsapp_request(payload)

async def mark_as_read(message_id: str):
    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id
    }
    return await send_whatsapp_request(payload)

async def send_interactive_buttons(to: str, body_text: str, buttons: list):
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": body_text},
            "action": {"buttons": buttons}
        }
    }
    return await send_whatsapp_request(payload)

async def send_media_message(to: str, media_type: str, media_url: str, caption: str = None, message_id: str = None):
    media_object = {}
    if media_type == 'image':
        media_object['image'] = {"link": media_url, "caption": caption}
    elif media_type == 'audio':
        media_object['audio'] = {"link": media_url}
    elif media_type == 'video':
        media_object['video'] = {"link": media_url, "caption": caption}
    elif media_type == 'document':
        media_object['document'] = {"link": media_url, "caption": caption, "filename": "info.pdf"}

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": media_type,
        **media_object
    }
    if message_id:
        payload["context"] = {"message_id": message_id}
    return await send_whatsapp_request(payload)