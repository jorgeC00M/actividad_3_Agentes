# src/entornos/entorno_recoleccion.py
import random
from typing import Set, Dict, Any, List, Tuple
from .entorno_base import EntornoBase


class EntornoRecoleccion(EntornoBase):
    """Entorno de recolección con comida y obstáculos (código original mejorado)"""
    
    def __init__(self, ancho: int, alto: int, num_comida: int = 10, num_obstaculos: int = 8):
        super().__init__(ancho, alto)
        self.comida: Dict[Tuple[int, int], int] = {}
        self.obstaculos: Set[Tuple[int, int]] = set()
        self._generar_comida(num_comida)
        self._generar_obstaculos(num_obstaculos)
    
    def _generar_comida(self, cantidad: int):
        """Genera comida aleatoria en el grid"""
        for _ in range(cantidad):
            x = random.randint(0, self.ancho - 1)
            y = random.randint(0, self.alto - 1)
            # Evitar superposición con obstáculos
            while (x, y) in self.obstaculos:
                x = random.randint(0, self.ancho - 1)
                y = random.randint(0, self.alto - 1)
            self.comida[(x, y)] = random.randint(1, 3)  # Valor de la comida
    
    def _generar_obstaculos(self, cantidad: int):
        """Genera obstáculos aleatorios en el grid"""
        for _ in range(cantidad):
            x = random.randint(0, self.ancho - 1)
            y = random.randint(0, self.alto - 1)
            self.obstaculos.add((x, y))
    
    def hay_comida(self, x: int, y: int) -> bool:
        """Verifica si hay comida en una posición"""
        return (x, y) in self.comida
    
    def hay_obstaculo(self, x: int, y: int) -> bool:
        """Verifica si hay un obstáculo en la posición"""
        return (x, y) in self.obstaculos
    
    def recolectar_comida(self, x: int, y: int) -> bool:
        """Recolecta comida de una posición"""
        if (x, y) in self.comida:
            del self.comida[(x, y)]
            return True
        return False
    
    def obtener_comida_cercana(self, x: int, y: int, radio: int = 5) -> List[Tuple[int, int]]:
        """Obtiene posiciones de comida dentro del radio"""
        comida_cercana = []
        for (fx, fy) in self.comida:
            distancia = abs(fx - x) + abs(fy - y)
            if distancia <= radio:
                comida_cercana.append((fx, fy))
        return comida_cercana
    
    def actualizar(self):
        """El entorno básico no cambia con el tiempo"""
        pass


class EntornoRecoleccionCompetitivo(EntornoRecoleccion):
    """Ejercicio 6: Entorno con recursos limitados para competencia"""
    
    def __init__(self, ancho: int, alto: int, num_comida: int = 5, num_obstaculos: int = 5):
        # Menos recursos para crear competencia
        super().__init__(ancho, alto, num_comida, num_obstaculos)
    
    def actualizar(self):
        """En entorno competitivo, la comida puede reaparecer lentamente"""
        if self.tiempo % 10 == 0 and len(self.comida) < 3:
            # Reponer algo de comida periódicamente
            self._generar_comida(1)