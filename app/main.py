from fastapi import FastAPI
from mangum import Mangum
from app.controllers import validation_controller

app = FastAPI()

# Registrar las rutas
app.include_router(validation_controller.router)

# Inicia el servidor con: uvicorn app.main:app --reload
handler = Mangum(app)