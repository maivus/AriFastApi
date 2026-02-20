import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Ari Chatbot"
    VERIFY_TOKEN: str = os.getenv("VERIFY_TOKEN")
    WHATSAPP_TOKEN: str = os.getenv("WHATSAPP_TOKEN")
    PHONE_NUMBER_ID: str = os.getenv("PHONE_NUMBER_ID")

settings = Settings()