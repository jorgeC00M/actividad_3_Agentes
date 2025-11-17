# src/entornos/entorno_limpieza.py
import random
from typing import Set, Dict, Any, Tuple, Optional

from .entorno_base import EntornoBase


class EntornoLimpieza(EntornoBase):
    """Entorno básico de limpieza."""

    def __init__(self, ancho: int, alto: int, num_suciedad: int):
        super().__init__(ancho, alto)
        self.suciedad: Set[Tuple[int, int]] = set()
        self._generar_suciedad(num_suciedad)

    def _generar_suciedad(self, cantidad: int):
        """Genera suciedad aleatoria en el grid."""
        for _ in range(cantidad):
            x = random.randint(0, self.ancho - 1)
            y = random.randint(0, self.alto - 1)
            self.suciedad.add((x, y))

    def hay_suciedad(self, x: int, y: int) -> bool:
        """Verifica si hay suciedad en una posición."""
        return (x, y) in self.suciedad

    def limpiar(self, x: int, y: int) -> bool:
        """Limpia suciedad en una posición."""
        if (x, y) in self.suciedad:
            self.suciedad.remove((x, y))
            return True
        return False

    def hay_obstaculo(self, x: int, y: int) -> bool:
        """Por defecto, no hay obstáculos."""
        return False

    def actualizar(self):
        """El entorno básico no cambia con el tiempo."""
        pass


class EntornoLimpiezaConTipos(EntornoLimpieza):
    """Ejercicio 2: Entorno con diferentes tipos de suciedad."""

    def __init__(
        self,
        ancho: int,
        alto: int,
        num_suciedad: int,
        tipos_suciedad: Dict[str, Dict[str, Any]] = None,
    ):
        super().__init__(ancho, alto, 0)  # No generar suciedad base
        self.suciedad: Dict[Tuple[int, int], Dict[str, Any]] = {}
        self.tipos_suciedad = tipos_suciedad or {
            "polvo": {"valor": 1, "simbolo": "P"},
            "mancha": {"valor": 2, "simbolo": "M"},
            "barro": {"valor": 3, "simbolo": "B"},
        }
        self._generar_suciedad_con_tipos(num_suciedad)

    def _generar_suciedad_con_tipos(self, cantidad: int):
        """Genera suciedad de diferentes tipos."""
        for _ in range(cantidad):
            x = random.randint(0, self.ancho - 1)
            y = random.randint(0, self.alto - 1)
            tipo = random.choice(list(self.tipos_suciedad.keys()))
            self.suciedad[(x, y)] = {
                "tipo": tipo,
                "valor": self.tipos_suciedad[tipo]["valor"],
            }

    def hay_suciedad(self, x: int, y: int) -> bool:
        return (x, y) in self.suciedad

    def limpiar(self, x: int, y: int) -> Optional[Tuple[str, int]]:
        """Limpia suciedad y retorna tipo y puntos."""
        if (x, y) in self.suciedad:
            tipo = self.suciedad[(x, y)]["tipo"]
            valor = self.suciedad[(x, y)]["valor"]
            del self.suciedad[(x, y)]
            return (tipo, valor)
        return None


class EntornoLimpiezaConObstaculos(EntornoLimpieza):
    """Ejercicio 3: Entorno con obstáculos fijos."""

    def __init__(
        self, ancho: int, alto: int, num_suciedad: int, num_obstaculos: int = 10
    ):
        super().__init__(ancho, alto, num_suciedad)
        self.obstaculos: Set[Tuple[int, int]] = set()
        self._generar_obstaculos(num_obstaculos)

    def _generar_obstaculos(self, cantidad: int):
        """Genera obstáculos aleatorios en el grid."""
        for _ in range(cantidad):
            x = random.randint(0, self.ancho - 1)
            y = random.randint(0, self.alto - 1)
            self.obstaculos.add((x, y))

    def hay_obstaculo(self, x: int, y: int) -> bool:
        """Verifica si hay un obstáculo en la posición."""
        return (x, y) in self.obstaculos
