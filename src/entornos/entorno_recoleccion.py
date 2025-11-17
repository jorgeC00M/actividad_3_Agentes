# src/entornos/entorno_recoleccion.py
import random
from typing import Set, Dict, List, Tuple

from .entorno_base import EntornoBase


class EntornoRecoleccion(EntornoBase):
    """Entorno de recolección con comida y obstáculos."""

    def __init__(
        self, ancho: int, alto: int, num_comida: int = 10, num_obstaculos: int = 8
    ):
        super().__init__(ancho, alto)
        self.comida: Dict[Tuple[int, int], int] = {}
        self.obstaculos: Set[Tuple[int, int]] = set()
        self._generar_obstaculos(num_obstaculos)
        self._generar_comida(num_comida)

    def _generar_obstaculos(self, cantidad: int):
        for _ in range(cantidad):
            x = random.randint(0, self.ancho - 1)
            y = random.randint(0, self.alto - 1)
            self.obstaculos.add((x, y))

    def _generar_comida(self, cantidad: int):
        for _ in range(cantidad):
            x = random.randint(0, self.ancho - 1)
            y = random.randint(0, self.alto - 1)
            while (x, y) in self.obstaculos:
                x = random.randint(0, self.ancho - 1)
                y = random.randint(0, self.alto - 1)
            self.comida[(x, y)] = random.randint(1, 3)

    def hay_comida(self, x: int, y: int) -> bool:
        return (x, y) in self.comida

    def hay_obstaculo(self, x: int, y: int) -> bool:
        return (x, y) in self.obstaculos

    def recolectar_comida(self, x: int, y: int) -> bool:
        if (x, y) in self.comida:
            del self.comida[(x, y)]
            return True
        return False

    def obtener_comida_cercana(
        self, x: int, y: int, radio: int = 5
    ) -> List[Tuple[int, int]]:
        comida_cercana: List[Tuple[int, int]] = []
        for (fx, fy) in self.comida:
            distancia = abs(fx - x) + abs(fy - y)
            if distancia <= radio:
                comida_cercana.append((fx, fy))
        return comida_cercana

    def actualizar(self):
        pass


class EntornoRecoleccionCompetitivo(EntornoRecoleccion):
    """Ejercicio 6: Entorno con pocos recursos para generar competencia."""

    def __init__(
        self, ancho: int, alto: int, num_comida: int = 5, num_obstaculos: int = 5
    ):
        super().__init__(ancho, alto, num_comida, num_obstaculos)

    def actualizar(self):
        # Reposición lenta de comida si casi no hay
        if self.tiempo % 10 == 0 and len(self.comida) < 3:
            self._generar_comida(1)
