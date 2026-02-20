import httpx
from app.config import settings  # Importamos nuestra nueva configuración segura

async def send_whatsapp_message(to_number: str, message_text: str):
    # Ahora usamos los valores centralizados en settings
    token = settings.WHATSAPP_TOKEN
    phone_id = settings.PHONE_NUMBER_ID
    
    # Construcción de la URL de la API de Meta
    url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message_text}
    }

    # Usamos httpx para el envío asíncrono
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status() # Lanza un error si la API de Meta responde mal
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"Error de la API de WhatsApp: {e.response.text}")
            return None
        except Exception as e:
            print(f"Error inesperado al enviar mensaje: {e}")
            return None