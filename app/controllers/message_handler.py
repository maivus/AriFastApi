import re
from app.services import whatsapp_service

# Gestión de estados en memoria
user_sessions = {}

class MessageHandler:
    async def handle_incoming_message(self, message: dict, sender_name: str):
        from_number = message.get("from")
        message_id = message.get("id")
        msg_type = message.get("type")

        if message_id:
            await whatsapp_service.mark_as_read(message_id)

        # --- LÓGICA DE FLUJO DE REGISTRO ACTIVO ---
        if msg_type == 'text' and from_number in user_sessions:
            text_body = message.get("text", {}).get("body", "")
            await self.handle_registration_flow(from_number, text_body, message_id)
            return

        # --- CASO A: Mensaje de TEXTO ---
        if msg_type == 'text':
            text_body = message.get("text", {}).get("body", "").lower().strip()
            
            if self.is_greeting(text_body):
                await self.send_welcome_message(from_number, message_id, sender_name)
                await self.send_welcome_menu(from_number)
            else:
                response = "¡Hola! 👋 Soy Ari. Por el momento no reconocí tu mensaje. Por favor inicia con un saludo."
                await whatsapp_service.send_message(from_number, response, message_id)

        # --- CASO B: Respuesta de BOTÓN ---
        elif msg_type == 'interactive':
            interactive = message.get("interactive", {})
            if interactive.get("type") == 'button_reply':
                button_id = interactive.get("button_reply", {}).get("id")
                await self.handle_button_action(button_id, from_number, message_id)

    async def handle_registration_flow(self, to: str, text: str, message_id: str):
        session = user_sessions[to]
        clean_text = text.strip()

        # Si el usuario está en un paso de confirmación, ignoramos nuevos textos
        if "CONFIRMING" in session['step']:
            await whatsapp_service.send_message(to, "Por favor, usa los botones de arriba para confirmar o corregir la información. 👆", message_id)
            return

        # Paso 1: Nombre
        if session['step'] == 'AWAITING_NAME':
            if not re.match(r"^[a-zA-ZÀ-ÿ\s]{3,}$", clean_text):
                await whatsapp_service.send_message(to, "❌ Nombre no válido. Por favor usa solo letras (mínimo 3).", message_id)
                return
            session['temp_data'] = clean_text
            session['step'] = 'CONFIRMING_NAME'
            await self.ask_confirmation(to, f"¿Confirmas que el nombre es:\n*{clean_text}*?", 'name')

        # Paso 2: Especialidad (Solo para Médicos)
        elif session['step'] == 'AWAITING_SPECIALTY':
            if len(clean_text) < 3:
                await whatsapp_service.send_message(to, "❌ Por favor, indica una especialidad válida.", message_id)
                return
            session['temp_data'] = clean_text
            session['step'] = 'CONFIRMING_SPECIALTY'
            await self.ask_confirmation(to, f"¿La especialidad es:\n*{clean_text}*?", 'specialty')

        # Paso 3: Dirección
        elif session['step'] == 'AWAITING_ADDRESS':
            if len(clean_text) < 5:
                await whatsapp_service.send_message(to, "❌ La dirección es muy corta. Por favor sé más específico.", message_id)
                return
            session['temp_data'] = clean_text
            session['step'] = 'CONFIRMING_ADDRESS'
            await self.ask_confirmation(to, f"¿Confirmas la dirección:\n*{clean_text}*?", 'address')

    async def ask_confirmation(self, to, body_text, confirm_type):
        buttons = [
            {"type": "reply", "reply": {"id": f"yes_{confirm_type}", "title": "Sí, es correcto ✅"}},
            {"type": "reply", "reply": {"id": f"no_{confirm_type}", "title": "No, corregir ✍️"}}
        ]
        await whatsapp_service.send_interactive_buttons(to, body_text, buttons)

    async def handle_button_action(self, button_id, to, message_id):
        session = user_sessions.get(to)

        # --- OPCIONES DEL MENÚ INICIAL ---
        if button_id == 'option_1':
            reg_buttons = [
                {"type": "reply", "reply": {"id": "reg_medico", "title": "Médico 👨‍⚕️"}},
                {"type": "reply", "reply": {"id": "reg_farmacia", "title": "Farmacia 🏥"}}
            ]
            await whatsapp_service.send_interactive_buttons(to, "¡Perfecto! ¿Qué deseas registrar hoy?", reg_buttons)
        
        elif button_id == 'reg_medico':
            user_sessions[to] = {'step': 'AWAITING_NAME', 'type': 'medico', 'data': {}}
            await whatsapp_service.send_message(to, "Iniciemos. ¿Cuál es el nombre completo del médico? 📝")

        elif button_id == 'reg_farmacia':
            user_sessions[to] = {'step': 'AWAITING_NAME', 'type': 'farmacia', 'data': {}}
            await whatsapp_service.send_message(to, "Iniciemos. ¿Cuál es el nombre de la farmacia? 📝")

        # --- MANEJO DE CONFIRMACIONES (BOTONES) ---
        elif session:
            # Confirmación de Nombre
            if button_id == 'yes_name':
                session['data']['nombre'] = session['temp_data']
                if session['type'] == 'medico':
                    session['step'] = 'AWAITING_SPECIALTY'
                    await whatsapp_service.send_message(to, "¡Excelente! Ahora, ¿cuál es su especialidad? 🎓")
                else:
                    session['step'] = 'AWAITING_ADDRESS'
                    await whatsapp_service.send_message(to, "¡Excelente! Ahora, ingresa la dirección de la farmacia: 📍")
            
            elif button_id == 'no_name':
                session['step'] = 'AWAITING_NAME'
                await whatsapp_service.send_message(to, "De acuerdo. Escribe el nombre nuevamente: 📝")

            # Confirmación de Especialidad
            elif button_id == 'yes_specialty':
                session['data']['especialidad'] = session['temp_data']
                session['step'] = 'AWAITING_ADDRESS'
                await whatsapp_service.send_message(to, "Entendido. Finalmente, ingresa la dirección del consultorio: 📍")
            
            elif button_id == 'no_specialty':
                session['step'] = 'AWAITING_SPECIALTY'
                await whatsapp_service.send_message(to, "De acuerdo. Escribe la especialidad nuevamente: 🎓")

            # Confirmación de Dirección (FINAL)
            elif button_id == 'yes_address':
                session['data']['direccion'] = session['temp_data']
                # Aquí podrías hacer el guardado en base de datos en el futuro
                await whatsapp_service.send_message(to, "¡Gracias! Toda la información ha sido recolectada. El equipo de sistemas se contactará contigo cuando el registro esté creado. ✅")
                await self.send_welcome_menu(to)
                del user_sessions[to]
            
            elif button_id == 'no_address':
                session['step'] = 'AWAITING_ADDRESS'
                await whatsapp_service.send_message(to, "De acuerdo. Escribe la dirección nuevamente: 📍")

    def is_greeting(self, text):
        greetings = ["hola", "buenas", "que tal", "buenos dias", "buenas tardes", "buenas noches"]
        return any(g in text for g in greetings)

    async def send_welcome_message(self, to, message_id, sender_name):
        welcome = f"¡Hola {sender_name}! Soy Ari, gracias por ponerte en contacto conmigo."
        await whatsapp_service.send_message(to, welcome, message_id)

    async def send_welcome_menu(self, to):
        menu_buttons = [
            {"type": "reply", "reply": {"id": "option_1", "title": "Creación"}},
            {"type": "reply", "reply": {"id": "option_2", "title": "Información 💡"}},
            {"type": "reply", "reply": {"id": "option_3", "title": "Hablar con Humano"}}
        ]
        await whatsapp_service.send_interactive_buttons(to, "¿En qué te puedo ayudar?", menu_buttons)

handler = MessageHandler()