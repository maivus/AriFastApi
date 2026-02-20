from fastapi import FastAPI
from app.routers import messages  # Importamos tu archivo de rutas

app = FastAPI(title="Ari Chatbot")

# Conectamos las rutas del archivo messages.py
app.include_router(messages.router)

@app.get("/")
def inicio():
    return {"status": "Servidor funcionando correctamente"}