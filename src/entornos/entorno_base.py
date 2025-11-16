"""Clase base para entornos tipo grid."""

from abc import ABC, abstractmethod
from typing import Tuple


class EntornoBase(ABC):
    """Clase base abstracta para entornos tipo grid 2D."""
    
    def __init__(self, ancho: int, alto: int):
        """
        Inicializa el entorno base.
        
        Args:
            ancho: Ancho del grid
            alto: Alto del grid
        """
        self.ancho = ancho
        self.alto = alto
        self.paso_actual = 0
    
    def es_posicion_valida(self, x: int, y: int) -> bool:
        """
        Verifica si una posición está dentro de los límites.
        
        Args:
            x: Coordenada x
            y: Coordenada y
            
        Returns:
            True si es válida
        """
        return 0 <= x < self.ancho and 0 <= y < self.alto
    
    @abstractmethod
    def reset(self) -> None:
        """Reinicia el entorno a su estado inicial."""
        pass
    
    @abstractmethod
    def step(self) -> None:
        """Avanza un paso en la simulación."""
        pass
    
    def get_dimensiones(self) -> Tuple[int, int]:
        """Retorna las dimensiones del entorno."""
        return (self.ancho, self.alto)
