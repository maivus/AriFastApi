import httpx
from app.config import settings

async def send_whatsapp_request(payload: dict):
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
            print(f"Error en WhatsApp API: {e}")
            return None

async def send_message(to: str, text: str, message_id: str = None):
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    if message_id: payload["context"] = {"message_id": message_id}
    return await send_whatsapp_request(payload)

async def mark_as_read(message_id: str):
    payload = {"messaging_product": "whatsapp", "status": "read", "message_id": message_id}
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