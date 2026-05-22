# Router de productos: CRUD con paginación, autenticación y restricción por rol admin.
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.producto_repository import ProductoRepository
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoOut
from app.factories.response_factory import ResponseFactory, APIResponse, PaginatedResponse
from app.factories.link_builder import LinkBuilder
from app.core.security import get_current_user, require_rol
from app.core.audit import registrar
from app.models.usuario import Usuario

router = APIRouter(prefix="/productos", tags=["Productos"])

# Dependencia: instancia el repositorio con la sesión de BD inyectada.
# Patrón Repository: separa la lógica de acceso a datos de la lógica del endpoint.
def get_repo(db: Session = Depends(get_db)) -> ProductoRepository:
    return ProductoRepository(db)


# POST /productos/ — crea un nuevo producto. Solo admins pueden crear productos.
@router.post("/", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(data: ProductoCreate, repo: ProductoRepository = Depends(get_repo), usuario: Usuario = Depends(require_rol("admin"))):
    producto = repo.create(data)
    registrar("CREAR", "productos", f"id={producto.id} nombre='{producto.nombre}'", usuario.email)
    return ResponseFactory.created(ProductoOut.model_validate(producto), "Producto creado exitosamente", LinkBuilder.producto(producto.id))


# GET /productos/ — lista productos activos con paginación. Cualquier usuario autenticado puede consultar.
# Query parameters con validación: page >= 1, limit entre 1 y 100.
@router.get("/", response_model=PaginatedResponse)
def listar_productos(
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(10, ge=1, le=100, description="Productos por página"),
    repo: ProductoRepository = Depends(get_repo),
    _=Depends(get_current_user),
):
    resultado = repo.get_all_paginated(page, limit)
    # LinkBuilder agrega links de navegación (prev/next) según la página actual.
    return ResponseFactory.paginated(
        data=[ProductoOut.model_validate(p) for p in resultado["data"]],
        total=resultado["total"],
        page=resultado["page"],
        limit=resultado["limit"],
        pages=resultado["pages"],
        links=LinkBuilder.productos_lista(resultado["page"], resultado["limit"], resultado["pages"]),
    )


# GET /productos/{producto_id} — obtiene un producto por ID.
@router.get("/{producto_id}", response_model=APIResponse)
def obtener_producto(producto_id: int, repo: ProductoRepository = Depends(get_repo), _=Depends(get_current_user)):
    producto = repo.get_by_id(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return ResponseFactory.success(ProductoOut.model_validate(producto), "Producto encontrado", LinkBuilder.producto(producto_id))


# PUT /productos/{producto_id} — actualiza un producto. Solo admins.
@router.put("/{producto_id}", response_model=APIResponse)
def actualizar_producto(producto_id: int, data: ProductoUpdate, repo: ProductoRepository = Depends(get_repo), usuario: Usuario = Depends(require_rol("admin"))):
    producto = repo.get_by_id(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    actualizado = repo.update(producto, data)
    # Se loguea qué campos se modificaron para trazabilidad en auditoría.
    registrar("ACTUALIZAR", "productos", f"id={producto_id} campos={list(data.model_dump(exclude_unset=True).keys())}", usuario.email)
    return ResponseFactory.success(ProductoOut.model_validate(actualizado), "Producto actualizado exitosamente", LinkBuilder.producto(producto_id))


# DELETE /productos/{producto_id} — soft delete. Solo admins.
@router.delete("/{producto_id}", response_model=APIResponse)
def eliminar_producto(producto_id: int, repo: ProductoRepository = Depends(get_repo), usuario: Usuario = Depends(require_rol("admin"))):
    producto = repo.get_by_id(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    repo.soft_delete(producto)
    registrar("ELIMINAR", "productos", f"id={producto_id} nombre='{producto.nombre}'", usuario.email)
    return ResponseFactory.success(message="Producto desactivado exitosamente")
