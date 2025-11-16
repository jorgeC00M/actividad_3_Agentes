"""Entorno de limpieza con suciedad y obstáculos."""

from typing import Dict, Set, Tuple
import random
from .entorno_base import EntornoBase


class EntornoLimpieza(EntornoBase):
    """
    Entorno de limpieza para ejercicios 1-3.
    
    Características:
    - Grid 2D con suciedad
    - Tipos de suciedad con diferentes valores (Ejercicio 2)
    - Obstáculos fijos (Ejercicio 3)
    """
    
    def __init__(
        self,
        ancho: int = 10,
        alto: int = 10,
        num_suciedad: int = 15,
        num_obstaculos: int = 5,
        tipos_suciedad: bool = True
    ):
        """
        Inicializa el entorno de limpieza.
        
        Args:
            ancho: Ancho del grid
            alto: Alto del grid
            num_suciedad: Cantidad inicial de suciedad
            num_obstaculos: Cantidad de obstáculos
            tipos_suciedad: Si usar tipos de suciedad diferentes
        """
        super().__init__(ancho, alto)
        
        self.num_suciedad_inicial = num_suciedad
        self.num_obstaculos = num_obstaculos
        self.tipos_suciedad = tipos_suciedad
        
        # Ejercicio 2: Tipos de suciedad
        self.tipos_disponibles = {
            'polvo': {'simbolo': '💨', 'valor': 1},
            'mugre': {'simbolo': '💩', 'valor': 3},
            'basura': {'simbolo': '🗑️', 'valor': 5}
        }
        
        # Estado del entorno
        self.suciedad: Dict[Tuple[int, int], Dict] = {}
        self.obstaculos: Set[Tuple[int, int]] = set()
        
        self.reset()
    
    def reset(self) -> None:
        """Reinicia el entorno."""
        self.suciedad.clear()
        self.obstaculos.clear()
        self.paso_actual = 0
        
        # Generar obstáculos
        for _ in range(self.num_obstaculos):
            while True:
                x, y = random.randint(0, self.ancho - 1), random.randint(0, self.alto - 1)
                if (x, y) not in self.obstaculos:
                    self.obstaculos.add((x, y))
                    break
        
        # Generar suciedad
        for _ in range(self.num_suciedad_inicial):
            while True:
                x, y = random.randint(0, self.ancho - 1), random.randint(0, self.alto - 1)
                if (x, y) not in self.obstaculos and (x, y) not in self.suciedad:
                    # Ejercicio 2: Asignar tipo de suciedad
                    if self.tipos_suciedad:
                        tipo = random.choice(list(self.tipos_disponibles.keys()))
                    else:
                        tipo = 'polvo'
                    
                    self.suciedad[(x, y)] = {
                        'tipo': tipo,
                        'valor': self.tipos_disponibles[tipo]['valor'],
                        'simbolo': self.tipos_disponibles[tipo]['simbolo']
                    }
                    break
    
    def hay_suciedad(self, x: int, y: int) -> bool:
        """Verifica si hay suciedad en una posición."""
        return (x, y) in self.suciedad
    
    def hay_obstaculo(self, x: int, y: int) -> bool:
        """Verifica si hay un obstáculo en una posición."""
        return (x, y) in self.obstaculos
    
    def obtener_info_suciedad(self, x: int, y: int) -> Dict:
        """Obtiene información de la suciedad en una posición."""
        return self.suciedad.get((x, y), {'tipo': None, 'valor': 0, 'simbolo': ''})
    
    def limpiar(self, x: int, y: int) -> Dict:
        """
        Limpia la suciedad en una posición.
        
        Returns:
            Dict con información de lo limpiado
        """
        if (x, y) in self.suciedad:
            info = self.suciedad.pop((x, y))
            return {
                'limpiado': True,
                'tipo': info['tipo'],
                'valor': info['valor']
            }
        return {'limpiado': False, 'tipo': None, 'valor': 0}
    
    def step(self) -> None:
        """Avanza un paso (puede usarse para suciedad dinámica)."""
        self.paso_actual += 1
    
    def get_suciedad_restante(self) -> int:
        """Retorna la cantidad de suciedad restante."""
        return len(self.suciedad)
    
    def render(self, agentes: list = None) -> str:
        """
        Genera representación visual del entorno.
        
        Args:
            agentes: Lista de agentes a mostrar
            
        Returns:
            String con representación del grid
        """
        grid = []
        agentes_pos = {(a.x, a.y): a for a in (agentes or [])}
        
        for y in range(self.alto):
            fila = []
            for x in range(self.ancho):
                if (x, y) in agentes_pos:
                    fila.append('🤖')
                elif (x, y) in self.obstaculos:
                    fila.append('🧱')
                elif (x, y) in self.suciedad:
                    fila.append(self.suciedad[(x, y)]['simbolo'])
                else:
                    fila.append('⬜')
            grid.append(' '.join(fila))
        
        return '\n'.join(grid)