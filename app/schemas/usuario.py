# Schemas Pydantic para autenticación y gestión de usuarios.
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Schema para registrar un nuevo usuario; el rol es opcional y por defecto "cajero".
class UsuarioCreate(BaseModel):
    nombre: str
    apellido: str
    email: str
    password: str           # Contraseña en texto plano; se hashea en el repositorio antes de guardar.
    rol: Optional[str] = "cajero"


# Schema de salida: nunca incluye el password_hash por seguridad.
class UsuarioOut(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    rol: str
    activo: bool
    fecha_registro: datetime

    model_config = {"from_attributes": True}


# Schema para el body del endpoint POST /auth/login.
class LoginRequest(BaseModel):
    email: str
    password: str


# Schema de respuesta del login: incluye el token JWT y los datos del usuario autenticado.
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"   # Siempre "bearer" según el estándar OAuth2.
    usuario: UsuarioOut
