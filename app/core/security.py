# Módulo de seguridad: maneja hashing de contraseñas, creación/validación de JWT
# y las dependencias de FastAPI para autenticación (JWT y API Key).
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from sqlalchemy.orm import Session
from app.database import get_db

# Clave secreta para firmar los JWT. En producción debe estar en una variable de entorno.
SECRET_KEY = "cambia-esta-clave-secreta-en-produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # El token expira en 1 hora.

# API Key estática como alternativa de autenticación (en producción usar variable de entorno).
API_KEY = "mi-api-key-secreta-2026"

# CryptContext con bcrypt a 12 rondas: buen balance entre seguridad y velocidad de hashing.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12, bcrypt__truncate_error=False)
# oauth2_scheme extrae el token del header "Authorization: Bearer <token>".
# auto_error=False permite que la dependencia reciba None si no se envía token (para soportar API Key también).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def hash_password(password: str) -> str:
    # Genera el hash bcrypt de la contraseña para almacenarlo de forma segura.
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    # Compara la contraseña en texto plano con el hash almacenado. Retorna True si coinciden.
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict) -> str:
    # Crea un JWT firmado con la SECRET_KEY. Agrega la fecha de expiración al payload.
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    # Decodifica y valida el JWT. Lanza 401 si el token es inválido o está expirado.
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    api_key: str = Security(api_key_header),
    db: Session = Depends(get_db),
):
    """Autentica por JWT o por API Key. Soporta ambos métodos simultáneamente."""
    from app.models.usuario import Usuario

    # Autenticación por API Key: busca cualquier usuario activo como representante de la clave.
    if api_key and api_key == API_KEY:
        user = db.query(Usuario).filter(Usuario.activo == True).first()
        if user:
            return user

    # Autenticación por JWT: decodifica el token y recupera el usuario por su ID.
    if token:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if user_id:
            user = db.query(Usuario).filter(Usuario.id == int(user_id)).first()
            if user:
                return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autenticado. Usa JWT o X-API-Key.",
    )


def require_rol(*roles: str):
    """Fábrica de dependencias que restringe el acceso a usuarios con el rol indicado."""
    def verificar(usuario=Depends(get_current_user)):
        if usuario.rol not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acción restringida. Se requiere rol: {' o '.join(roles)}",
            )
        return usuario
    return verificar
