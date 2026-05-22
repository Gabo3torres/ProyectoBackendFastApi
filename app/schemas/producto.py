# Schemas Pydantic para validación y serialización de datos de productos.
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# Schema para crear un producto: nombre y precio son obligatorios; stock inicia en 0 por defecto.
class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int = 0


# Schema para actualizar un producto: todos los campos son opcionales para permitir edición parcial.
# También permite cambiar activo=True para reactivar un producto eliminado.
class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    activo: Optional[bool] = None


# Schema de salida con todos los datos del producto que se devuelven en la API.
class ProductoOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    precio: float
    stock: int
    activo: bool
    fecha_registro: datetime

    model_config = {"from_attributes": True}


# Schema para respuestas paginadas: envuelve la lista de productos con metadatos de paginación.
class ProductosPaginados(BaseModel):
    total: int   # Total de registros en la BD (no solo en esta página).
    page: int    # Página actual.
    limit: int   # Productos por página.
    pages: int   # Total de páginas calculadas.
    data: List[ProductoOut]
