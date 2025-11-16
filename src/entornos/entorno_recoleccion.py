"""Entorno de recolección con comida y múltiples agentes."""

from typing import Dict, Set, Tuple, List, Any
import random
from .entorno_base import EntornoBase


class EntornoRecoleccion(EntornoBase):
    """
    Entorno de recolección para ejercicios 4-6.
    
    Características:
    - Comida distribuida en el grid
    - Soporte para múltiples agentes
    - Recursos limitados (Ejercicio 6: competencia)
    """
    
    def __init__(
        self,
        ancho: int = 15,
        alto: int = 15,
        num_comida: int = 20,
        competitivo: bool = False
    ):
        """
        Inicializa el entorno de recolección.
        
        Args:
            ancho: Ancho del grid
            alto: Alto del grid
            num_comida: Cantidad de comida
            competitivo: Si es modo competitivo
        """
        super().__init__(ancho, alto)
        
        self.num_comida_inicial = num_comida
        self.competitivo = competitivo
        
        # Estado
        self.comida: Set[Tuple[int, int]] = set()
        self.agentes: List[Any] = []
        
        self.reset()
    
    def reset(self) -> None:
        """Reinicia el entorno."""
        self.comida.clear()
        self.paso_actual = 0
        
        # Generar comida aleatoria
        for _ in range(self.num_comida_inicial):
            while True:
                x = random.randint(0, self.ancho - 1)
                y = random.randint(0, self.alto - 1)
                if (x, y) not in self.comida:
                    self.comida.add((x, y))
                    break
    
    def agregar_agente(self, agente: Any) -> None:
        """Agrega un agente al entorno."""
        self.agentes.append(agente)
    
    def hay_comida(self, x: int, y: int) -> bool:
        """Verifica si hay comida en una posición."""
        return (x, y) in self.comida
    
    def recolectar_comida(self, x: int, y: int) -> bool:
        """
        Recolecta comida en una posición.
        
        Returns:
            True si se recolectó comida
        """
        if (x, y) in self.comida:
            self.comida.remove((x, y))
            return True
        return False
    
    def obtener_agentes_en(self, x: int, y: int, radio: int = 1) -> List[Any]:
        """
        Obtiene agentes en un radio de una posición.
        
        Args:
            x: Coordenada x
            y: Coordenada y
            radio: Radio de búsqueda
            
        Returns:
            Lista de agentes en el radio
        """
        agentes_cercanos = []
        for agente in self.agentes:
            dist = abs(agente.x - x) + abs(agente.y - y)
            if dist <= radio:
                agentes_cercanos.append(agente)
        return agentes_cercanos
    
    def step(self) -> None:
        """Avanza un paso en la simulación."""
        self.paso_actual += 1
        
        # Ejercicio 6: Regenerar comida aleatoriamente en modo competitivo
        if self.competitivo and random.random() < 0.1:
            if len(self.comida) < self.num_comida_inicial:
                x = random.randint(0, self.ancho - 1)
                y = random.randint(0, self.alto - 1)
                self.comida.add((x, y))
    
    def get_comida_restante(self) -> int:
        """Retorna la cantidad de comida restante."""
        return len(self.comida)
    
    def render(self, agentes: list = None) -> str:
        """
        Genera representación visual del entorno.
        
        Args:
            agentes: Lista de agentes a mostrar
            
        Returns:
            String con representación del grid
        """
        grid = []
        agentes_a_mostrar = agentes or self.agentes
        agentes_pos = {}
        
        # Manejar múltiples agentes en la misma posición
        for a in agentes_a_mostrar:
            pos = (a.x, a.y)
            if pos not in agentes_pos:
                agentes_pos[pos] = []
            agentes_pos[pos].append(a)
        
        for y in range(self.alto):
            fila = []
            for x in range(self.ancho):
                if (x, y) in agentes_pos:
                    # Si hay múltiples agentes, mostrar número
                    num = len(agentes_pos[(x, y)])
                    if num > 1:
                        fila.append(f'{num}🤖')
                    else:
                        fila.append('🤖')
                elif (x, y) in self.comida:
                    fila.append('🍎')
                else:
                    fila.append('⬜')
            grid.append(' '.join(fila))
        
        return '\n'.join(grid)