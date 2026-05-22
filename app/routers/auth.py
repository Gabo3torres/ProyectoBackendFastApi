# Router de autenticación: expone los endpoints de registro y login de usuarios.
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import UsuarioCreate, LoginRequest, UsuarioOut
from app.factories.response_factory import ResponseFactory, APIResponse
from app.core.security import verify_password, create_access_token
from app.core.audit import registrar

# prefix="/auth" → todas las rutas de este router empiezan con /auth
# tags=["Autenticación"] → agrupa los endpoints en la documentación Swagger
router = APIRouter(prefix="/auth", tags=["Autenticación"])


# Dependencia de inyección: FastAPI crea automáticamente el repositorio con la sesión de BD.
def get_repo(db: Session = Depends(get_db)) -> UsuarioRepository:
    return UsuarioRepository(db)


# POST /auth/register — crea un nuevo usuario en el sistema.
@router.post("/register", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(data: UsuarioCreate, repo: UsuarioRepository = Depends(get_repo)):
    # Verifica que el email no esté ya registrado antes de crear.
    if repo.get_by_email(data.email):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    usuario = repo.create(data)
    # Se registra la acción en el archivo de auditoría.
    registrar("REGISTRO", "usuarios", f"id={usuario.id} rol={usuario.rol}", usuario.email)
    return ResponseFactory.created(UsuarioOut.model_validate(usuario), "Usuario registrado exitosamente")


# POST /auth/login — valida credenciales y devuelve un token JWT si son correctas.
@router.post("/login", response_model=APIResponse)
def login(data: LoginRequest, repo: UsuarioRepository = Depends(get_repo)):
    usuario = repo.get_by_email(data.email)
    # Se verifica que el usuario exista y que la contraseña coincida con el hash almacenado.
    if not usuario or not verify_password(data.password, usuario.password_hash):
        registrar("LOGIN_FAIL", "usuarios", "credenciales incorrectas", data.email)
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    if not usuario.activo:
        raise HTTPException(status_code=403, detail="Usuario inactivo")
    # Se genera el JWT con el id del usuario como subject ("sub").
    token = create_access_token({"sub": str(usuario.id)})
    registrar("LOGIN_OK", "usuarios", f"id={usuario.id} rol={usuario.rol}", usuario.email)
    return ResponseFactory.success(
        data={"access_token": token, "token_type": "bearer", "usuario": UsuarioOut.model_validate(usuario)},
        message="Login exitoso",
    )
