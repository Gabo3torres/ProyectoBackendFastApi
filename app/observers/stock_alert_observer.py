# Observador de alertas de stock: escucha el evento "venta_creada" y emite un warning
# en el log cuando el stock de algún producto baja del umbral mínimo definido.
import logging
from app.observers.base import Observer

logger = logging.getLogger("stock_alert")
# Umbral mínimo de stock: si un producto tiene 3 o menos unidades se emite una alerta.
STOCK_MINIMO = 3


class StockAlertObserver(Observer):
    """Alerta cuando el stock de un producto baja del umbral mínimo."""

    def update(self, evento: str, datos: dict) -> None:
        # Solo reacciona al evento de creación de ventas.
        if evento != "venta_creada":
            return
        # Revisa el stock restante de cada producto vendido en la venta.
        for item in datos.get("items", []):
            stock_restante = item["stock_restante"]
            if stock_restante <= STOCK_MINIMO:
                # El warning aparece en la consola del servidor para que el operador lo vea.
                logger.warning(
                    f"[STOCK BAJO] Producto '{item['nombre']}' "
                    f"— stock restante: {stock_restante} unidad(es)"
                )
