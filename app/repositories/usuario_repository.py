# Importaciones: Session para la BD, el modelo ORM, el schema de creación
# y la función que hashea contraseñas antes de guardarlas.
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.core.security import hash_password


# Repositorio de usuarios: solo operaciones de lectura y creación.
# No hay update ni delete porque la gestión de usuarios no está expuesta como endpoint CRUD completo.
class UsuarioRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Usuario | None:
        # Usado en login para buscar el usuario y en registro para detectar emails duplicados.
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    def get_by_id(self, usuario_id: int) -> Usuario | None:
        # Usado al decodificar el JWT para recuperar el objeto usuario completo.
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def create(self, data: UsuarioCreate) -> Usuario:
        usuario = Usuario(
            nombre=data.nombre,
            apellido=data.apellido,
            email=data.email,
            # La contraseña NUNCA se guarda en texto plano: se almacena el hash bcrypt.
            password_hash=hash_password(data.password),
            # Si el rol enviado no es válido, se asigna "cajero" como valor por defecto seguro.
            rol=data.rol if data.rol in ("admin", "cajero") else "cajero",
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
