# Archivo de prueba inicial (hello world).
# No forma parte de la aplicación principal; fue el primer endpoint creado en el proyecto.
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def inicio():
    return {"message": "¡Bienvenido a la API!"}
