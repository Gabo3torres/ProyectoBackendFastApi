# Importaciones de SQLAlchemy para definir columnas y tipos de datos,
# relationship para relaciones entre tablas, datetime para la fecha por defecto,
# y Base como clase padre de todos los modelos ORM del proyecto.
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


# Modelo ORM que mapea la tabla "clientes" en la base de datos.
# Cada atributo de clase corresponde a una columna de la tabla.
class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    # El email es opcional (nullable=True) pero único cuando se proporciona.
    email = Column(String(100), unique=True, nullable=True)
    telefono = Column(String(20), nullable=True)
    direccion = Column(String(200), nullable=True)
    # activo=False en lugar de borrar el registro (soft delete).
    activo = Column(Boolean, default=True)
    # Se asigna automáticamente la fecha UTC al crear el registro.
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    # Relación 1-N: un cliente puede tener muchas ventas.
    # back_populates enlaza con el atributo "cliente" del modelo Venta.
    ventas = relationship("Venta", back_populates="cliente")
