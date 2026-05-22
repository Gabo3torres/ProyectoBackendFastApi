# Modelos ORM para las tablas "ventas" y "detalle_ventas".
# Se usan ForeignKey para las relaciones entre tablas y cascade para borrado en cadena.
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


# Una Venta agrupa uno o más DetalleVenta y pertenece a un usuario (cajero) y opcionalmente a un cliente.
class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    # cliente_id es nullable: se permite venta anónima (mostrador sin cliente registrado).
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)
    # usuario_id es obligatorio: siempre debe haber un cajero autenticado que registre la venta.
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    total = Column(Float, nullable=False, default=0.0)
    observacion = Column(String(300), nullable=True)
    fecha = Column(DateTime, default=datetime.utcnow)

    # Relaciones ORM: permiten acceder a cliente.ventas y venta.detalles sin queries manuales.
    cliente = relationship("Cliente", back_populates="ventas")
    usuario = relationship("Usuario")
    # cascade="all, delete-orphan": si se borra la venta, se borran sus detalles automáticamente.
    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")


# Cada DetalleVenta representa un producto dentro de una venta (línea de ticket).
class DetalleVenta(Base):
    __tablename__ = "detalle_ventas"

    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    # Se guarda el precio al momento de la compra para que el historial no cambie si el precio sube.
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)  # precio_unitario * cantidad

    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles")
