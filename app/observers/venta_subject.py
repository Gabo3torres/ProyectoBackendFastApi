# VentaSubject: sujeto observable especializado en eventos de ventas.
# Al iniciarse suscribe automáticamente los dos observadores del sistema:
# StockAlertObserver (alertas de stock) y AuditLogObserver (auditoría).
from app.observers.base import Subject
from app.observers.stock_alert_observer import StockAlertObserver
from app.observers.audit_log_observer import AuditLogObserver


class VentaSubject(Subject):
    """Sujeto observable para el evento de creación de ventas."""

    def __init__(self):
        super().__init__()
        # Los observadores se suscriben en la construcción para que estén listos desde el inicio.
        self.suscribir(StockAlertObserver())
        self.suscribir(AuditLogObserver())

    def venta_creada(self, venta, usuario_email: str, items_detalle: list) -> None:
        # Empaqueta los datos relevantes de la venta y notifica a todos los observadores.
        self.notificar("venta_creada", {
            "venta_id": venta.id,
            "usuario_email": usuario_email,
            "total": venta.total,
            "items": items_detalle,
        })


# Instancia global compartida: se importa directamente en el repositorio para notificar eventos.
# Se crea una sola vez al iniciar la app (singleton implícito por el módulo de Python).
venta_subject = VentaSubject()
