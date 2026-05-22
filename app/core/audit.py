# Módulo de auditoría: registra en un archivo de log cada acción relevante de la API
# (crear, actualizar, eliminar, login exitoso/fallido) con timestamp y usuario responsable.
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Logger dedicado exclusivamente al archivo de auditoría; aislado del log general de consola.
audit_logger = logging.getLogger("auditoria")
audit_logger.setLevel(logging.INFO)
audit_logger.propagate = False  # Evita que los mensajes se dupliquen en la consola.

# RotatingFileHandler rota el archivo cuando supera 1 MB y conserva hasta 3 backups (audit.log.1, .2, .3).
_handler = RotatingFileHandler(
    "audit.log",
    maxBytes=1_000_000,
    backupCount=3,
    encoding="utf-8",
)
# Se usa solo el mensaje como formato para que cada línea sea legible sin prefijos de logging.
_handler.setFormatter(logging.Formatter("%(message)s"))
audit_logger.addHandler(_handler)


def registrar(accion: str, recurso: str, detalle: str, usuario: str = "sistema") -> None:
    # Construye una línea de auditoría con columnas alineadas para facilitar su lectura y parseo.
    # Formato: [2026-01-15 10:30:00] | CREAR      | clientes     | usuario: admin@mail.com       | id=5
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{timestamp}] | {accion:<10} | {recurso:<12} | usuario: {usuario:<30} | {detalle}"
    audit_logger.info(linea)
