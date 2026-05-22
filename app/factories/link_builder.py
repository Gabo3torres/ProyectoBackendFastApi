# LinkBuilder: fábrica de links HATEOAS (Hypermedia as the Engine of Application State).
# HATEOAS es un principio REST que devuelve junto a cada recurso los links de las acciones disponibles,
# permitiendo que el cliente navegue la API sin necesidad de conocer las URLs de antemano.
from app.factories.response_factory import Link

BASE = "http://127.0.0.1:8000"  # URL base de la API; cambiar en producción.


class LinkBuilder:
    """Construye los links HATEOAS para cada recurso de la API."""

    @staticmethod
    def producto(producto_id: int) -> list[Link]:
        # Links disponibles al operar sobre un producto individual.
        return [
            Link(rel="self",   href=f"{BASE}/productos/{producto_id}", method="GET"),
            Link(rel="update", href=f"{BASE}/productos/{producto_id}", method="PUT"),
            Link(rel="delete", href=f"{BASE}/productos/{producto_id}", method="DELETE"),
            Link(rel="list",   href=f"{BASE}/productos/",             method="GET"),
        ]

    @staticmethod
    def productos_lista(page: int, limit: int, pages: int) -> list[Link]:
        # Links de paginación: solo agrega "prev" y "next" cuando corresponde.
        links = [
            Link(rel="self",   href=f"{BASE}/productos/?page={page}&limit={limit}", method="GET"),
            Link(rel="create", href=f"{BASE}/productos/",                           method="POST"),
        ]
        if page > 1:
            links.append(Link(rel="prev", href=f"{BASE}/productos/?page={page - 1}&limit={limit}", method="GET"))
        if page < pages:
            links.append(Link(rel="next", href=f"{BASE}/productos/?page={page + 1}&limit={limit}", method="GET"))
        return links

    @staticmethod
    def cliente(cliente_id: int) -> list[Link]:
        return [
            Link(rel="self",   href=f"{BASE}/clientes/{cliente_id}", method="GET"),
            Link(rel="update", href=f"{BASE}/clientes/{cliente_id}", method="PUT"),
            Link(rel="delete", href=f"{BASE}/clientes/{cliente_id}", method="DELETE"),
            Link(rel="list",   href=f"{BASE}/clientes/",            method="GET"),
        ]

    @staticmethod
    def clientes_lista() -> list[Link]:
        return [
            Link(rel="self",   href=f"{BASE}/clientes/", method="GET"),
            Link(rel="create", href=f"{BASE}/clientes/", method="POST"),
        ]

    @staticmethod
    def venta(venta_id: int) -> list[Link]:
        # Las ventas no tienen update ni delete porque son transacciones inmutables.
        return [
            Link(rel="self", href=f"{BASE}/ventas/{venta_id}", method="GET"),
            Link(rel="list", href=f"{BASE}/ventas/",           method="GET"),
        ]

    @staticmethod
    def ventas_lista() -> list[Link]:
        return [
            Link(rel="self",   href=f"{BASE}/ventas/", method="GET"),
            Link(rel="create", href=f"{BASE}/ventas/", method="POST"),
        ]
