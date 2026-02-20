from app.services import whatsapp_service
from app.controllers.flows.registration import registration_flow
from app.controllers.flows.welcome import welcome_flow
from app.controllers.flows.information import info_flow
from app.controllers.flows.support import support_flow

class MessageHandler:
    async def handle_incoming_message(self, message: dict, sender_name: str):
        # 1. Extracción de datos básicos
        from_number = message.get("from")
        message_id = message.get("id")
        msg_type = message.get("type")

        # 2. Marcar como leído automáticamente
        if message_id: 
            await whatsapp_service.mark_as_read(message_id)

        # 3. INTERCEPTOR: ¿El usuario está a mitad de un registro?
        # Si está en la lista de sesiones activas, todo el tráfico va directo a registration_flow
        if from_number in registration_flow.user_sessions:
            if msg_type == 'text':
                await registration_flow.handle_text(from_number, message['text']['body'], message_id)
            elif msg_type == 'interactive':
                btn_id = message['interactive']['button_reply']['id']
                await registration_flow.handle_button(from_number, btn_id, message_id)
            return # Salimos para que no evalúe saludos ni menús

        # 4. ENRUTADOR DE TEXTO LIBRE (Nuevas interacciones)
        if msg_type == 'text':
            text_body = message.get("text", {}).get("body", "")
            
            # Verificamos si es un saludo usando el módulo welcome_flow
            if welcome_flow.is_greeting(text_body):
                await welcome_flow.send_welcome_menu(from_number, sender_name)
            else:
                await whatsapp_service.send_message(
                    from_number, 
                    "No estoy segura de cómo ayudarte con eso. Intenta escribir 'Hola' para ver las opciones.", 
                    message_id
                )

        # 5. ENRUTADOR DE BOTONES (Menú Principal y Submenús)
        elif msg_type == 'interactive':
            button_id = message['interactive']['button_reply']['id']
            await self.route_button_action(button_id, from_number, message_id)

    async def route_button_action(self, btn_id: str, to: str, message_id: str):
        """
        Este método es el Traffic Controller. Solo redirige, no crea respuestas.
        """
        
        # --- ENRUTAMIENTO DINÁMICO (Por Prefijo) ---
        # Todo botón que empiece con "reg_" inicia un flujo de registro
        if btn_id.startswith('reg_'):
            reg_type = btn_id.replace('reg_', '') # Extrae 'medico' o 'farmacia'
            await registration_flow.start_flow(to, reg_type)
            return

        # --- ENRUTAMIENTO ESTÁTICO (Menú Principal) ---
        if btn_id == 'option_1': # Botón de Creación
            await welcome_flow.send_creation_menu(to)
            
        elif btn_id == 'option_2': # Botón de Información
            await info_flow.send_info_menu(to)
            
        elif btn_id == 'option_3': # Botón de Humano
            await support_flow.start_human_support(to)
            
        else:
            print(f"⚠️ Alerta de enrutamiento: Botón no reconocido ({btn_id})")

# Instancia única para ser importada en el router principal (messages.py)
handler = MessageHandler()