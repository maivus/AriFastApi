from app.services import whatsapp_service

class WelcomeFlow:
    def is_greeting(self, text: str) -> bool:
        greetings = ["hola", "buenas", "que tal", "buenos dias", "tardes", "noches", "inicio"]
        return any(g in text.lower().strip() for g in greetings)

    async def send_welcome_menu(self, to: str, name: str):
        welcome_text = f"¡Hola *{name}*! 👋 Soy Ari, tu asistente de Aropharmait."
        
        buttons = [
            {"type": "reply", "reply": {"id": "option_1", "title": "Creación 📝"}},
            {"type": "reply", "reply": {"id": "option_2", "title": "Información 💡"}},
            {"type": "reply", "reply": {"id": "option_3", "title": "Hablar con Humano"}}
        ]
        
        await whatsapp_service.send_message(to, welcome_text)
        await whatsapp_service.send_interactive_buttons(to, "¿En qué puedo ayudarte hoy?", buttons)

welcome_flow = WelcomeFlow()