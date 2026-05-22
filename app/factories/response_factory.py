# ResponseFactory: patrón Factory que garantiza una estructura de respuesta uniforme en toda la API.
# Todos los endpoints devuelven el mismo envelope JSON: success, message, data, links, timestamp.
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel


# Modelo de un link HATEOAS: describe una acción disponible sobre el recurso.
class Link(BaseModel):
    rel: str     # Relación del link (self, update, delete, next, prev...).
    href: str    # URL del endpoint.
    method: str  # Método HTTP (GET, POST, PUT, DELETE).


# Estructura estándar para respuestas simples (éxito o error).
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None          # Payload variable: puede ser un objeto, lista o None.
    links: Optional[list[Link]] = None  # Links HATEOAS opcionales.
    timestamp: str                      # Fecha/hora UTC de la respuesta en formato ISO 8601.


# Estructura extendida para respuestas con paginación; agrega metadatos de la página.
class PaginatedResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    total: int    # Total de registros en la BD.
    page: int     # Página actual.
    limit: int    # Elementos por página.
    pages: int    # Total de páginas disponibles.
    links: Optional[list[Link]] = None
    timestamp: str


class ResponseFactory:
    """Fábrica que garantiza respuestas con estructura uniforme en toda la API."""

    @staticmethod
    def _now() -> str:
        # Timestamp en formato ISO 8601 sin microsegundos.
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def success(data: Any = None, message: str = "Operación exitosa", links: list[Link] | None = None) -> APIResponse:
        # Respuesta 200 OK genérica para consultas y actualizaciones.
        return APIResponse(
            success=True,
            message=message,
            data=data,
            links=links,
            timestamp=ResponseFactory._now(),
        )

    @staticmethod
    def created(data: Any = None, message: str = "Registro creado exitosamente", links: list[Link] | None = None) -> APIResponse:
        # Respuesta para recursos creados (HTTP 201); misma estructura que success.
        return APIResponse(
            success=True,
            message=message,
            data=data,
            links=links,
            timestamp=ResponseFactory._now(),
        )

    @staticmethod
    def paginated(data: Any, total: int, page: int, limit: int, pages: int, links: list[Link] | None = None) -> PaginatedResponse:
        # Respuesta para listas paginadas; incluye metadatos necesarios para la navegación del cliente.
        return PaginatedResponse(
            success=True,
            message="Consulta exitosa",
            data=data,
            total=total,
            page=page,
            limit=limit,
            pages=pages,
            links=links,
            timestamp=ResponseFactory._now(),
        )

    @staticmethod
    def error(message: str = "Ocurrió un error") -> APIResponse:
        # Respuesta de error estandarizada (usada internamente; FastAPI maneja la mayoría via HTTPException).
        return APIResponse(
            success=False,
            message=message,
            data=None,
            links=None,
            timestamp=ResponseFactory._now(),
        )
