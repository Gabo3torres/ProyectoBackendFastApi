# Punto de entrada principal de la aplicación FastAPI.
# Configura logging, crea las tablas en la BD, registra los routers y aplica middleware CORS.
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

# Configuración global de logging: muestra nivel, nombre del logger y mensaje en consola.
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s",
)

# Los modelos deben importarse antes de create_all para que SQLAlchemy los registre en Base.metadata.
import app.models.usuario
import app.models.cliente
import app.models.producto
import app.models.venta
from app.routers import auth, clientes, productos, ventas

# Crea todas las tablas en la BD si aún no existen (no borra datos existentes).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="POS Backend",
    description="API para sistema de punto de venta con login, clientes, productos y ventas.",
    version="1.0.0",
)

# CORS abierto para desarrollo. En producción se deben listar solo los orígenes permitidos.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de routers: cada uno agrupa los endpoints de su recurso con su propio prefix y tags.
app.include_router(auth.router)
app.include_router(clientes.router)
app.include_router(productos.router)
app.include_router(ventas.router)


# Endpoint raíz: confirma que la API está activa y dirige a la documentación automática.
@app.get("/", tags=["Root"])
def root():
    return {"message": "POS API activa", "docs": "/docs"}
