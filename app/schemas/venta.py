# Schemas Pydantic para el proceso de ventas.
# Se separan los schemas de entrada (In) y salida (Out) para controlar qué datos acepta y devuelve la API.
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# Schema de entrada para cada ítem de la venta: qué producto y cuántas unidades.
class DetalleVentaIn(BaseModel):
    producto_id: int
    cantidad: int


# Schema de salida para cada ítem de la venta: incluye el precio y subtotal calculados.
class DetalleVentaOut(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float   # Precio fijado al momento de la venta.
    subtotal: float          # precio_unitario * cantidad

    model_config = {"from_attributes": True}


# Schema para crear una venta: el cliente es opcional (venta anónima permitida).
# items debe tener al menos un elemento; esa validación se hace en el router.
class VentaCreate(BaseModel):
    cliente_id: Optional[int] = None
    observacion: Optional[str] = None
    items: List[DetalleVentaIn]


# Schema de salida completo de la venta incluyendo todos sus detalles.
class VentaOut(BaseModel):
    id: int
    cliente_id: Optional[int]
    usuario_id: int          # ID del cajero que registró la venta.
    total: float
    observacion: Optional[str]
    fecha: datetime
    detalles: List[DetalleVentaOut]

    model_config = {"from_attributes": True}
