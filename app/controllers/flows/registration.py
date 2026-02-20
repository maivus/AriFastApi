import re
from app.services import whatsapp_service
from app.controllers.flows.welcome import welcome_flow

class RegistrationFlow:
    def __init__(self):
        self.user_sessions = {}

    async def handle_text(self, to: str, text: str, message_id: str):
        session = self.user_sessions.get(to)
        if not session or "CONFIRMING" in session['step']: return

        clean_text = text.strip()

        if session['step'] == 'AWAITING_NAME':
            if not re.match(r"^[a-zA-ZÀ-ÿ\s]{3,}$", clean_text):
                await whatsapp_service.send_message(to, "❌ Nombre no válido. Mínimo 3 letras.", message_id)
                return
            session['temp_data'] = clean_text
            session['step'] = 'CONFIRMING_NAME'
            await self.ask_confirmation(to, f"¿Confirmas el nombre:\n*{clean_text}*?", 'name')

        elif session['step'] == 'AWAITING_SPECIALTY':
            if len(clean_text) < 3:
                await whatsapp_service.send_message(to, "❌ Indica una especialidad válida.", message_id)
                return
            session['temp_data'] = clean_text
            session['step'] = 'CONFIRMING_SPECIALTY'
            await self.ask_confirmation(to, f"¿La especialidad es:\n*{clean_text}*?", 'specialty')

        elif session['step'] == 'AWAITING_ADDRESS':
            if len(clean_text) < 5:
                await whatsapp_service.send_message(to, "❌ La dirección es muy corta.", message_id)
                return
            session['temp_data'] = clean_text
            session['step'] = 'CONFIRMING_ADDRESS'
            await self.ask_confirmation(to, f"¿Confirmas la dirección:\n*{clean_text}*?", 'address')

    async def handle_button(self, to: str, button_id: str, message_id: str):
        session = self.user_sessions.get(to)
        if not session: return

        # Lógica de SI/NO para cada paso
        if button_id == 'yes_name':
            session['data']['nombre'] = session['temp_data']
            if session['type'] == 'medico':
                session['step'] = 'AWAITING_SPECIALTY'
                await whatsapp_service.send_message(to, "¡Excelente! ¿Cuál es su especialidad? 🎓")
            else:
                session['step'] = 'AWAITING_ADDRESS'
                await whatsapp_service.send_message(to, "¡Excelente! Ingresa la dirección de la farmacia: 📍")
        
        elif button_id == 'no_name':
            session['step'] = 'AWAITING_NAME'
            await whatsapp_service.send_message(to, "Escribe el nombre nuevamente: 📝")

        elif button_id == 'yes_specialty':
            session['data']['especialidad'] = session['temp_data']
            session['step'] = 'AWAITING_ADDRESS'
            await whatsapp_service.send_message(to, "Entendido. Finalmente, ingresa la dirección del consultorio: 📍")

        elif button_id == 'yes_address':
            session['data']['direccion'] = session['temp_data']
            await whatsapp_service.send_message(to, "✅ Registro completado. El equipo de sistemas procesará la info.")
            del self.user_sessions[to] # Limpiar sesión

    async def ask_confirmation(self, to, body_text, confirm_type):
        buttons = [
            {"type": "reply", "reply": {"id": f"yes_{confirm_type}", "title": "Sí, es correcto ✅"}},
            {"type": "reply", "reply": {"id": f"no_{confirm_type}", "title": "No, corregir ✍️"}}
        ]
        await whatsapp_service.send_interactive_buttons(to, body_text, buttons)
        await welcome_flow.send_menu(to, "¿Deseas realizar alguna otra acción?")
        
    async def start_flow(self, to: str, reg_type: str):
        """Inicializa la sesión y envía el primer mensaje del formulario"""
        self.user_sessions[to] = {'step': 'AWAITING_NAME', 'type': reg_type, 'data': {}}
        
        tipo_texto = "Médico" if reg_type == 'medico' else "Farmacia"
        await whatsapp_service.send_message(to, f"Iniciemos el registro de {tipo_texto}. ¿Cuál es el nombre? 📝")

registration_flow = RegistrationFlow()