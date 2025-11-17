# src/agentes/agente_base.py
from abc import ABC, abstractmethod
from typing import Any, Optional


class AgenteBase(ABC):
    """Clase base abstracta para todos los agentes del sistema."""

    def __init__(self, x: int, y: int, agent_id: Optional[str] = None):
        self.x = x
        self.y = y
        self.id = agent_id or f"agente_{id(self)}"
        self.energia = 100
        self.activo = True

    @abstractmethod
    def percibir(self, entorno) -> Any:
        """Recibe información del entorno."""
        ...

    @abstractmethod
    def decidir(self, percepcion: Any) -> str:
        """Toma una decisión basada en la percepción."""
        ...

    @abstractmethod
    def actuar(self, decision: str, entorno) -> None:
        """Ejecuta una acción en el entorno."""
        ...

    def ciclo_vida(self, entorno) -> bool:
        """
        Ejecuta el ciclo completo de percepción-decisión-acción.
        Devuelve False si el agente ya no está activo.
        """
        if not self.activo or self.energia <= 0:
            return False

        percepcion = self.percibir(entorno)
        decision = self.decidir(percepcion)
        self.actuar(decision, entorno)
        return True

    def mover(self, direccion: str, entorno) -> bool:
        """Intenta mover el agente en una dirección."""
        direcciones = {
            "arriba": (0, -1),
            "abajo": (0, 1),
            "izquierda": (-1, 0),
            "derecha": (1, 0),
        }

        if direccion not in direcciones:
            return False

        dx, dy = direcciones[direccion]
        nuevo_x, nuevo_y = self.x + dx, self.y + dy

        hay_obstaculo = getattr(entorno, "hay_obstaculo", lambda *_: False)

        if entorno.es_valida(nuevo_x, nuevo_y) and not hay_obstaculo(nuevo_x, nuevo_y):
            self.x, self.y = nuevo_x, nuevo_y
            self.energia -= 1
            return True
        return False

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.id} @ {self.x},{self.y})"
