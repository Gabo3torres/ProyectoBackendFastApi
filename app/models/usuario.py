# Modelo ORM para la tabla de usuarios del sistema.
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database import Base

# Roles válidos del sistema: "admin" tiene acceso total, "cajero" solo puede consultar y vender.
ROLES = ("admin", "cajero")


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    # El email es el identificador de login; debe ser único e indexado para búsquedas rápidas.
    email = Column(String(100), unique=True, nullable=False, index=True)
    # Nunca se guarda la contraseña en texto plano; solo el hash bcrypt.
    password_hash = Column(String(255), nullable=False)
    # Rol por defecto "cajero" para limitar permisos en caso de error de asignación.
    rol = Column(String(20), nullable=False, default="cajero")
    activo = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
