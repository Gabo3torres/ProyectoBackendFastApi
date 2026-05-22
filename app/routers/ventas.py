# Router de ventas: registrar nuevas ventas y consultar el historial.
# La creación valida stock antes de persistir para evitar ventas con inventario insuficiente.
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.venta_repository import VentaRepository
from app.schemas.venta import VentaCreate, VentaOut
from app.factories.response_factory import ResponseFactory, APIResponse
from app.factories.link_builder import LinkBuilder
from app.core.security import get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/ventas", tags=["Ventas"])


# Dependencia: instancia el repositorio con la sesión de BD.
def get_repo(db: Session = Depends(get_db)) -> VentaRepository:
    return VentaRepository(db)


# POST /ventas/ — registra una nueva venta. Cualquier usuario autenticado puede vender.
@router.post("/", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def crear_venta(data: VentaCreate, repo: VentaRepository = Depends(get_repo), usuario: Usuario = Depends(get_current_user)):
    # La venta debe tener al menos un producto.
    if not data.items:
        raise HTTPException(status_code=400, detail="La venta debe tener al menos un producto")

    # Se valida stock ANTES de crear cualquier registro para evitar ventas parciales inconsistentes.
    for item in data.items:
        producto = repo.get_producto(item.producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto {item.producto_id} no encontrado")
        if producto.stock < item.cantidad:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para '{producto.nombre}'")

    # Solo si todos los ítems pasan la validación se persiste la venta y se descuenta el stock.
    venta = repo.create(data.cliente_id, usuario.id, data.observacion, data.items, usuario.email)
    return ResponseFactory.created(VentaOut.model_validate(venta), "Venta registrada exitosamente", LinkBuilder.venta(venta.id))


# GET /ventas/ — lista todas las ventas ordenadas de más reciente a más antigua.
@router.get("/", response_model=APIResponse)
def listar_ventas(repo: VentaRepository = Depends(get_repo), _=Depends(get_current_user)):
    ventas = repo.get_all()
    return ResponseFactory.success([VentaOut.model_validate(v) for v in ventas], f"{len(ventas)} venta(s) encontrada(s)", LinkBuilder.ventas_lista())


# GET /ventas/{venta_id} — obtiene el detalle completo de una venta por ID.
@router.get("/{venta_id}", response_model=APIResponse)
def obtener_venta(venta_id: int, repo: VentaRepository = Depends(get_repo), _=Depends(get_current_user)):
    venta = repo.get_by_id(venta_id)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return ResponseFactory.success(VentaOut.model_validate(venta), "Venta encontrada", LinkBuilder.venta(venta_id))
