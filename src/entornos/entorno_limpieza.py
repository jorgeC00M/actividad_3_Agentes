# src/entornos/entorno_limpieza.py
import random
from typing import Set, Dict, Any, Tuple, Optional

from .entorno_base import EntornoBase


class EntornoLimpieza(EntornoBase):
    """Entorno básico de limpieza con suciedad simple (sin tipos)."""

    def __init__(self, ancho: int, alto: int, num_suciedad: int):
        super().__init__(ancho, alto)
        self.suciedad: Set[Tuple[int, int]] = set()
        self._generar_suciedad(num_suciedad)

    def _generar_suciedad(self, cantidad: int):
        for _ in range(cantidad):
            x = random.randint(0, self.ancho - 1)
            y = random.randint(0, self.alto - 1)
            self.suciedad.add((x, y))

    def hay_suciedad(self, x: int, y: int) -> bool:
        return (x, y) in self.suciedad

    def limpiar(self, x: int, y: int) -> bool:
        if (x, y) in self.suciedad:
            self.suciedad.remove((x, y))
            return True
        return False

    def hay_obstaculo(self, x: int, y: int) -> bool:
        return False

    def actualizar(self):
        pass


class EntornoLimpiezaConTipos(EntornoLimpieza):
    """Ejercicio 2: Entorno con diferentes tipos de suciedad y valor asociado."""

    def __init__(
        self,
        ancho: int,
        alto: int,
        num_suciedad: int,
        tipos_suciedad: Dict[str, Dict[str, Any]] = None,
    ):
        super().__init__(ancho, alto, 0)  # no generes suciedad simple
        self.suciedad: Dict[Tuple[int, int], Dict[str, Any]] = {}
        self.tipos_suciedad = tipos_suciedad or {
            "polvo": {"valor": 1, "simbolo": "P"},
            "mancha": {"valor": 2, "simbolo": "M"},
            "barro": {"valor": 3, "simbolo": "B"},
        }
        self._generar_suciedad_con_tipos(num_suciedad)

    def _generar_suciedad_con_tipos(self, cantidad: int):
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
        if (x, y) in self.suciedad:
            tipo = self.suciedad[(x, y)]["tipo"]
            valor = self.suciedad[(x, y)]["valor"]
            del self.suciedad[(x, y)]
            return tipo, valor
        return None


class EntornoLimpiezaConObstaculos(EntornoLimpieza):
    """Ejercicio 3: Entorno de limpieza con obstáculos fijos."""

    def __init__(
        self, ancho: int, alto: int, num_suciedad: int, num_obstaculos: int = 10
    ):
        super().__init__(ancho, alto, num_suciedad)
        self.obstaculos: Set[Tuple[int, int]] = set()
        self._generar_obstaculos(num_obstaculos)

    def _generar_obstaculos(self, cantidad: int):
        for _ in range(cantidad):
            x = random.randint(0, self.ancho - 1)
            y = random.randint(0, self.alto - 1)
            self.obstaculos.add((x, y))

    def hay_obstaculo(self, x: int, y: int) -> bool:
        return (x, y) in self.obstaculos
