from app.services import whatsapp_service

class SupportFlow:
    async def start_human_support(self, to: str):
        text = (
            "🙋 *Atención Humana*\n\n"
            "He notificado a uno de nuestros agentes. En breve se pondrán en contacto "
            "contigo a través de este chat.\n\n"
            "Horario de atención: Lun-Vie, 8:00 AM - 5:00 PM."
        )
        await whatsapp_service.send_message(to, text)
        # Aquí es donde en el futuro podrías disparar un email o alerta a un dashboard

support_flow = SupportFlow()