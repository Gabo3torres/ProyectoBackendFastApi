# Importaciones: ceil para calcular páginas, Session para la conexión a la BD,
# el modelo ORM y los schemas de validación de entrada.
from sqlalchemy.orm import Session
from math import ceil
from app.models.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate


# Repositorio que centraliza todas las queries relacionadas con Producto.
class ProductoRepository:

    def __init__(self, db: Session):
        # Se guarda la sesión para reutilizarla en todos los métodos.
        self.db = db

    def get_all_paginated(self, page: int, limit: int) -> dict:
        # Solo devuelve productos activos; calcula el total antes de paginar.
        query = self.db.query(Producto).filter(Producto.activo == True)
        total = query.count()
        # offset desplaza los registros según la página solicitada.
        items = query.offset((page - 1) * limit).limit(limit).all()
        return {
            "total": total,
            "page": page,
            "limit": limit,
            # Si no hay resultados se devuelve al menos 1 página para evitar división por cero.
            "pages": ceil(total / limit) if total else 1,
            "data": items,
        }

    def get_by_id(self, producto_id: int) -> Producto | None:
        # Retorna None si el producto no existe (no lanza excepción, eso lo hace el router).
        return self.db.query(Producto).filter(Producto.id == producto_id).first()

    def create(self, data: ProductoCreate) -> Producto:
        # model_dump() convierte el schema Pydantic a un dict compatible con el modelo ORM.
        producto = Producto(**data.model_dump())
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)  # Recupera el id y otros valores generados por la BD.
        return producto

    def update(self, producto: Producto, data: ProductoUpdate) -> Producto:
        # exclude_unset=True ignora los campos que el cliente no envió en el request.
        for campo, valor in data.model_dump(exclude_unset=True).items():
            setattr(producto, campo, valor)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def soft_delete(self, producto: Producto) -> None:
        # No se elimina físicamente: solo se marca como inactivo para conservar historial de ventas.
        producto.activo = False
        self.db.commit()
