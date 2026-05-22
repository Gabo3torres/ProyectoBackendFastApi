# Router de clientes: CRUD completo con autenticación JWT/API Key y control de roles.
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteOut
from app.factories.response_factory import ResponseFactory, APIResponse
from app.factories.link_builder import LinkBuilder
from app.core.security import get_current_user, require_rol
from app.core.audit import registrar
from app.models.usuario import Usuario

router = APIRouter(prefix="/clientes", tags=["Clientes"])

# Dependencia que instancia el repositorio con la sesión de BD inyectada por FastAPI.
# Patrón Repository: separa la lógica de acceso a datos de la lógica del endpoint.
def get_repo(db: Session = Depends(get_db)) -> ClienteRepository:
    return ClienteRepository(db)


# POST /clientes/ — crea un nuevo cliente. Requiere usuario autenticado (cualquier rol).
@router.post("/", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def crear_cliente(data: ClienteCreate, repo: ClienteRepository = Depends(get_repo), usuario: Usuario = Depends(get_current_user)):
    # Validación de email duplicado solo cuando se proporciona email.
    if data.email and repo.get_by_email(data.email):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    cliente = repo.create(data)
    registrar("CREAR", "clientes", f"id={cliente.id} nombre='{cliente.nombre} {cliente.apellido}'", usuario.email)
    # LinkBuilder genera los links HATEOAS para navegar los recursos relacionados.
    return ResponseFactory.created(ClienteOut.model_validate(cliente), "Cliente creado exitosamente", LinkBuilder.cliente(cliente.id))


# GET /clientes/ — lista todos los clientes activos. Requiere autenticación.
@router.get("/", response_model=APIResponse)
def listar_clientes(repo: ClienteRepository = Depends(get_repo), _=Depends(get_current_user)):
    clientes = repo.get_all()
    return ResponseFactory.success([ClienteOut.model_validate(c) for c in clientes], f"{len(clientes)} cliente(s) encontrado(s)", LinkBuilder.clientes_lista())


# GET /clientes/{cliente_id} — obtiene un cliente por su ID.
@router.get("/{cliente_id}", response_model=APIResponse)
def obtener_cliente(cliente_id: int, repo: ClienteRepository = Depends(get_repo), _=Depends(get_current_user)):
    cliente = repo.get_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return ResponseFactory.success(ClienteOut.model_validate(cliente), "Cliente encontrado", LinkBuilder.cliente(cliente_id))


# PUT /clientes/{cliente_id} — actualiza los datos de un cliente. Permite edición parcial.
@router.put("/{cliente_id}", response_model=APIResponse)
def actualizar_cliente(cliente_id: int, data: ClienteUpdate, repo: ClienteRepository = Depends(get_repo), _=Depends(get_current_user)):
    cliente = repo.get_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    actualizado = repo.update(cliente, data)
    return ResponseFactory.success(ClienteOut.model_validate(actualizado), "Cliente actualizado exitosamente", LinkBuilder.cliente(cliente_id))


# DELETE /clientes/{cliente_id} — soft delete. Solo accesible por rol "admin".
@router.delete("/{cliente_id}", response_model=APIResponse)
def eliminar_cliente(cliente_id: int, repo: ClienteRepository = Depends(get_repo), usuario: Usuario = Depends(require_rol("admin"))):
    cliente = repo.get_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    repo.soft_delete(cliente)
    registrar("ELIMINAR", "clientes", f"id={cliente_id}", usuario.email)
    return ResponseFactory.success(message="Cliente desactivado exitosamente")
