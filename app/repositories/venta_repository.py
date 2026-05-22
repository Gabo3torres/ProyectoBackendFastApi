# Importaciones: Session para la BD, modelos de Venta y Producto,
# y el sujeto observable que notifica a los observadores cuando se crea una venta.
from sqlalchemy.orm import Session
from app.models.venta import Venta, DetalleVenta
from app.models.producto import Producto
from app.observers.venta_subject import venta_subject


# Repositorio de ventas: maneja las queries y la lógica de negocio del proceso de venta
# (descuento de stock, cálculo del total y notificación de eventos).
class VentaRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Venta]:
        # Devuelve todas las ventas ordenadas de más reciente a más antigua.
        return self.db.query(Venta).order_by(Venta.fecha.desc()).all()

    def get_by_id(self, venta_id: int) -> Venta | None:
        return self.db.query(Venta).filter(Venta.id == venta_id).first()

    def get_producto(self, producto_id: int) -> Producto | None:
        # Solo retorna el producto si existe Y está activo (no se puede vender un producto eliminado).
        return self.db.query(Producto).filter(
            Producto.id == producto_id,
            Producto.activo == True
        ).first()

    def create(self, cliente_id, usuario_id: int, observacion: str | None, items: list, usuario_email: str = "") -> Venta:
        # Se crea la venta con total=0 temporalmente; se calculará al procesar cada ítem.
        venta = Venta(
            cliente_id=cliente_id,
            usuario_id=usuario_id,
            observacion=observacion,
            total=0.0,
        )
        self.db.add(venta)
        # flush() envía el INSERT a la BD sin hacer commit, así se obtiene venta.id
        # para poder usarlo en los DetalleVenta que se crean a continuación.
        self.db.flush()

        total = 0.0
        items_detalle = []  # Se acumulan para notificar a los observadores al final.

        for item in items:
            producto = self.get_producto(item.producto_id)
            subtotal = producto.precio * item.cantidad
            total += subtotal
            # Se descuenta el stock del producto en esta misma transacción.
            producto.stock -= item.cantidad
            self.db.add(DetalleVenta(
                venta_id=venta.id,
                producto_id=producto.id,
                cantidad=item.cantidad,
                precio_unitario=producto.precio,  # Se guarda el precio al momento de la venta.
                subtotal=subtotal,
            ))
            # Se acumula info para los observadores (auditoría y alerta de stock).
            items_detalle.append({
                "nombre": producto.nombre,
                "cantidad": item.cantidad,
                "stock_restante": producto.stock,
            })

        venta.total = total
        self.db.commit()
        self.db.refresh(venta)

        # Notifica a todos los observadores suscritos (AuditLogObserver y StockAlertObserver).
        venta_subject.venta_creada(venta, usuario_email, items_detalle)

        return venta
