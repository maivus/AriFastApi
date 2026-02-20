from app.services.whatsapp_service import send_whatsapp_message

async def process_message(data: dict):
    try:
        # Extracción segura de datos
        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [{}])

        if not messages:
            return

        msg = messages[0]
        from_number = msg.get("from")
        text_body = msg.get("text", {}).get("body", "").lower().strip()

        # Lógica de "Cerebro" de Ari
        response_text = ""

        if text_body in ["hola", "buenas", "inicio"]:
            response_text = "¡Hola Jorge! Soy Ari. ¿En qué puedo ayudarte hoy? 👋"
        
        elif "estado" in text_body:
            response_text = "Todos los sistemas están operativos en Render. 🚀"
        
        elif "precio" in text_body:
            response_text = "Para darte precios, necesito consultar la base de datos (próximamente). 📊"
        
        else:
            response_text = f"No estoy segura de qué significa '{text_body}', pero lo he anotado para aprender. 🧠"

        # Envío de la respuesta
        await send_whatsapp_message(from_number, response_text)

    except Exception as e:
        print(f"Error en el cerebro de Ari: {e}")