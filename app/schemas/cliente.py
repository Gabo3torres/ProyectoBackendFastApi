# Schemas Pydantic para validación y serialización de datos de clientes.
# Pydantic valida automáticamente los tipos y lanza errores 422 si los datos no cumplen.
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Schema para crear un nuevo cliente: solo nombre y apellido son obligatorios.
class ClienteCreate(BaseModel):
    nombre: str
    apellido: str
    email: Optional[str] = None      # Opcional para clientes sin email registrado.
    telefono: Optional[str] = None
    direccion: Optional[str] = None


# Schema para actualizar un cliente: todos los campos son opcionales (PATCH parcial).
# exclude_unset=True en el repositorio garantiza que solo se modifiquen los campos enviados.
class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    activo: Optional[bool] = None    # Permite reactivar un cliente previamente eliminado.


# Schema de salida: define exactamente qué campos se devuelven en la respuesta JSON.
# from_attributes=True permite construirlo desde un objeto ORM de SQLAlchemy.
class ClienteOut(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: Optional[str]
    telefono: Optional[str]
    direccion: Optional[str]
    activo: bool
    fecha_registro: datetime

    model_config = {"from_attributes": True}
