# Implementación del patrón de diseño Observer (publicador/suscriptor).
# Permite que múltiples objetos (observadores) reaccionen automáticamente cuando ocurre un evento
# en el sujeto (por ejemplo, cuando se crea una venta) sin que el sujeto conozca los observadores.
from abc import ABC, abstractmethod


# Interfaz abstracta que deben implementar todos los observadores.
# ABC (Abstract Base Class) garantiza que cualquier subclase implemente el método update.
class Observer(ABC):
    """Interfaz que deben implementar todos los observadores."""

    @abstractmethod
    def update(self, evento: str, datos: dict) -> None:
        # evento: nombre del evento ocurrido (ej. "venta_creada").
        # datos: diccionario con información relevante del evento.
        pass


# Clase base para cualquier objeto que pueda ser observado.
# Mantiene la lista de suscriptores y los notifica cuando ocurre un evento.
class Subject:
    """Clase base para cualquier sujeto observable."""

    def __init__(self):
        # Lista interna de observadores suscritos.
        self._observers: list[Observer] = []

    def suscribir(self, observer: Observer) -> None:
        # Agrega un observador a la lista de notificaciones.
        self._observers.append(observer)

    def desuscribir(self, observer: Observer) -> None:
        # Elimina un observador para que deje de recibir notificaciones.
        self._observers.remove(observer)

    def notificar(self, evento: str, datos: dict) -> None:
        # Recorre todos los observadores y les pasa el evento con sus datos.
        for observer in self._observers:
            observer.update(evento, datos)
