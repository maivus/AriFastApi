from app.services import whatsapp_service

class WelcomeFlow:
    def is_greeting(self, text: str) -> bool:
        greetings = ["hola", "buenas", "que tal", "buenos dias", "tardes", "noches", "inicio"]
        return any(g in text.lower().strip() for g in greetings)

    async def send_welcome_menu(self, to: str, name: str):
        # 1. Enviamos solo el saludo
        welcome_text = f"¡Hola *{name}*! 👋 Soy Ari, tu asistente de Aropharmait."
        await whatsapp_service.send_message(to, welcome_text)
        
        # 2. Invocamos la función del menú
        await self.send_menu(to, "¿En qué puedo ayudarte hoy?")

    async def send_menu(self, to: str, text: str):
        """Envía el menú principal con un texto personalizado"""
        buttons = [
            {"type": "reply", "reply": {"id": "option_1", "title": "Creación 📝"}},
            {"type": "reply", "reply": {"id": "option_2", "title": "Información 💡"}},
            {"type": "reply", "reply": {"id": "option_3", "title": "Hablar con Humano"}}
        ]
        await whatsapp_service.send_interactive_buttons(to, text, buttons)

    async def send_creation_menu(self, to: str):
        buttons = [
            {"type": "reply", "reply": {"id": "reg_medico", "title": "Médico 👨‍⚕️"}},
            {"type": "reply", "reply": {"id": "reg_farmacia", "title": "Farmacia 🏥"}}
        ]
        await whatsapp_service.send_interactive_buttons(to, "¡Perfecto! ¿Qué deseas registrar hoy?", buttons)

welcome_flow = WelcomeFlow()