# Columnas de SQLAlchemy incluyendo Float para el precio,
# relationship para la relación con los detalles de venta,
# y Base como clase padre del ORM.
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


# Modelo ORM que mapea la tabla "productos".
class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(300), nullable=True)
    precio = Column(Float, nullable=False)
    # stock inicia en 0; se reduce con cada venta y puede actualizarse manualmente.
    stock = Column(Integer, default=0)
    # Soft delete: activo=False oculta el producto sin borrar su historial de ventas.
    activo = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    # Relación 1-N con DetalleVenta: un producto puede aparecer en muchos detalles de venta.
    detalles = relationship("DetalleVenta", back_populates="producto")
