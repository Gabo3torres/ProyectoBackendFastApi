# Observador de auditoría: escucha el evento "venta_creada" y escribe una línea en audit.log
# con los detalles de la transacción (id, total, productos vendidos, cajero responsable).
from app.observers.base import Observer
from app.core.audit import registrar


class AuditLogObserver(Observer):
    """Registra en audit.log cada venta creada (disparado por el patrón Observer)."""

    def update(self, evento: str, datos: dict) -> None:
        # Solo reacciona al evento de creación de ventas; ignora cualquier otro evento.
        if evento != "venta_creada":
            return
        # Construye un resumen legible de los productos vendidos: "Café x2, Azúcar x1".
        productos = ", ".join(
            f"{i['nombre']} x{i['cantidad']}" for i in datos.get("items", [])
        )
        registrar(
            accion="VENTA",
            recurso="ventas",
            detalle=f"id={datos['venta_id']} total=${datos['total']:,.0f} productos=[{productos}]",
            usuario=datos["usuario_email"],
        )
