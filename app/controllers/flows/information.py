from app.services import whatsapp_service

class InformationFlow:
    async def send_info_menu(self, to: str):
        text = (
            "💡 *Información de Ari*\n\n"
            "Soy un asistente inteligente desarrollado para optimizar los procesos de "
            "Aropharma. Actualmente puedo ayudarte con:\n"
            "• Registro de Médicos y Farmacias.\n"
            "• Información básica de sistemas.\n"
            "• Enlace directo con soporte humano."
        )
        await whatsapp_service.send_message(to, text)
        # Aquí podrías enviar más botones si fuera necesario

info_flow = InformationFlow()