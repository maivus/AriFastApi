from fastapi import FastAPI
from app.routers import messages  # Importamos el archivo que acabamos de arreglar

# Inicializamos la app
app = FastAPI(
    title="Ari Chatbot API",
    description="Backend de Ari migrado de Node.js a FastAPI",
    version="2.0.0"
)

# Configuración importante: Esto ayuda a que FastAPI sea más flexible con las URLs
app.router.redirect_slashes = False

# Incluimos las rutas del webhook
# El prefijo ya está definido en el router, pero aquí lo confirmamos
app.include_router(messages.router)

@app.get("/")
async def root():
    return {
        "message": "Ari API está en línea",
        "plataforma": "FastAPI / Render",
        "status": "active"
    }