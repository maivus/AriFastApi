from app.services.whatsapp_service import send_whatsapp_message

async def process_message(data: dict):
    try:
        # Extraer la info del mensaje (como lo hacías en JS)
        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [{}])

        if messages:
            msg = messages[0]
            from_number = msg.get("from")
            text_body = msg.get("text", {}).get("body", "").lower()

            # Lógica de respuesta (puedes expandir esto con tus emojis)
            if "hola" in text_body:
                response_text = "¡Hola Jorge! Soy Ari en versión Python/FastAPI. 🐍"
            else:
                response_text = f"Recibí tu mensaje: '{text_body}'. Estoy aprendiendo Python todavía."

            # Enviamos la respuesta de vuelta
            await send_whatsapp_message(from_number, response_text)
            
    except Exception as e:
        print(f"Error procesando: {e}")