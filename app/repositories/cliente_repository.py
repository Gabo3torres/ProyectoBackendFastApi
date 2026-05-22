# Importaciones necesarias: Session de SQLAlchemy para manejar la conexión a la base de datos,
# el modelo Cliente (tabla de la BD) y los schemas para crear/actualizar clientes.
from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate


# Repositorio que encapsula todas las operaciones de base de datos relacionadas con Cliente.
# Recibe una sesión de BD en el constructor para ejecutar las queries.
class ClienteRepository:

    def __init__(self, db: Session):
        # Se guarda la sesión para usarla en todos los métodos del repositorio.
        self.db = db

    def get_all(self) -> list[Cliente]:
        # Retorna solo los clientes activos (soft delete: activo=True).
        return self.db.query(Cliente).filter(Cliente.activo == True).all()

    def get_by_id(self, cliente_id: int) -> Cliente | None:
        # Busca un cliente por su ID. Retorna None si no existe.
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def get_by_email(self, email: str) -> Cliente | None:
        # Busca un cliente por su email. Útil para validar duplicados o autenticación.
        return self.db.query(Cliente).filter(Cliente.email == email).first()

    def create(self, data: ClienteCreate) -> Cliente:
        # Convierte el schema a un modelo ORM, lo persiste y refresca para obtener el ID generado.
        cliente = Cliente(**data.model_dump())
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)  # Sincroniza el objeto con los valores que asignó la BD (ej. id, timestamps).
        return cliente

    def update(self, cliente: Cliente, data: ClienteUpdate) -> Cliente:
        # Actualiza solo los campos enviados en el request (exclude_unset ignora los campos no proporcionados).
        for campo, valor in data.model_dump(exclude_unset=True).items():
            setattr(cliente, campo, valor)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def soft_delete(self, cliente: Cliente) -> None:
        # Marca el cliente como inactivo en vez de borrarlo físicamente de la BD.
        cliente.activo = False
        self.db.commit()
