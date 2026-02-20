from app.services import whatsapp_service
from app.controllers.flows.registration import registration_flow

class MessageHandler:
    async def handle_incoming_message(self, message: dict, sender_name: str):
        from_number = message.get("from")
        message_id = message.get("id")
        msg_type = message.get("type")

        if message_id: await whatsapp_service.mark_as_read(message_id)

        # 1. Delegar si hay flujo de registro activo
        if from_number in registration_flow.user_sessions:
            if msg_type == 'text':
                await registration_flow.handle_text(from_number, message['text']['body'], message_id)
            elif msg_type == 'interactive':
                await registration_flow.handle_button(from_number, message['interactive']['button_reply']['id'], message_id)
            return

        # 2. Lógica Menú Principal
        if msg_type == 'text':
            text = message['text']['body'].lower().strip()
            if any(g in text for g in ["hola", "buenas"]):
                await self.send_main_menu(from_number, sender_name)
        
        elif msg_type == 'interactive':
            btn_id = message['interactive']['button_reply']['id']
            if btn_id == 'option_1':
                buttons = [
                    {"type": "reply", "reply": {"id": "reg_medico", "title": "Médico 👨‍⚕️"}},
                    {"type": "reply", "reply": {"id": "reg_farmacia", "title": "Farmacia 🏥"}}
                ]
                await whatsapp_service.send_interactive_buttons(from_number, "¿Qué deseas registrar?", buttons)
            elif btn_id in ['reg_medico', 'reg_farmacia']:
                tipo = 'medico' if btn_id == 'reg_medico' else 'farmacia'
                registration_flow.user_sessions[from_number] = {'step': 'AWAITING_NAME', 'type': tipo, 'data': {}}
                await whatsapp_service.send_message(from_number, f"Iniciemos el registro de {tipo}. ¿Nombre? 📝")

    async def send_main_menu(self, to, name):
        buttons = [
            {"type": "reply", "reply": {"id": "option_1", "title": "Creación"}},
            {"type": "reply", "reply": {"id": "option_3", "title": "Humano 🙋"}}
        ]
        await whatsapp_service.send_message(to, f"¡Hola {name}! Soy Ari.")
        await whatsapp_service.send_interactive_buttons(to, "¿En qué te ayudo?", buttons)

handler = MessageHandler()