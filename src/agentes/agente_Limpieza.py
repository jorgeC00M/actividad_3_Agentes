"""Agente de limpieza con memoria (Ejercicios 1-3)."""

from typing import Set, Tuple, Dict, List, Optional
import random
from .agente_base import AgenteBase


class AgenteLimpieza(AgenteBase):
    """
    Agente de limpieza que implementa:
    - Ejercicio 1: Memoria de lugares visitados
    - Ejercicio 2: Manejo de tipos de suciedad
    - Ejercicio 3: Evitación de obstáculos
    """
    
    def __init__(self, x: int = 0, y: int = 0, con_memoria: bool = True):
        """
        Inicializa el agente de limpieza.
        
        Args:
            x: Posición inicial en x
            y: Posición inicial en y
            con_memoria: Si debe recordar lugares visitados
        """
        super().__init__(None, x, y)
        
        # Ejercicio 1: Memoria de lugares visitados
        self.con_memoria = con_memoria
        self.visitados: Set[Tuple[int, int]] = {(x, y)}
        self.limpiados: Set[Tuple[int, int]] = set()
        
        # Ejercicio 2: Estadísticas por tipo de suciedad
        self.suciedad_limpiada = 0
        self.puntos_totales = 0
        self.suciedad_por_tipo: Dict[str, int] = {}
        
        # Ejercicio 3: Memoria de obstáculos
        self.obstaculos_conocidos: Set[Tuple[int, int]] = set()
        
        # Métricas
        self.movimientos = 0
        self.acciones_limpieza = 0
    
    def percibir(self, entorno: Any) -> Dict:
        """
        Percibe el entorno de limpieza.
        
        Returns:
            Dict con información del entorno
        """
        percepcion = {
            'hay_suciedad': entorno.hay_suciedad(self.x, self.y),
            'tipo_suciedad': None,
            'valor_suciedad': 0,
            'vecinos_validos': [],
            'vecinos_no_visitados': [],
            'hay_obstaculo': False
        }
        
        # Obtener información de suciedad si existe
        if percepcion['hay_suciedad']:
            suciedad_info = entorno.obtener_info_suciedad(self.x, self.y)
            percepcion['tipo_suciedad'] = suciedad_info['tipo']
            percepcion['valor_suciedad'] = suciedad_info['valor']
        
        # Obtener vecinos válidos (sin obstáculos)
        direcciones = [
            (0, -1, 'arriba'),
            (0, 1, 'abajo'),
            (-1, 0, 'izquierda'),
            (1, 0, 'derecha')
        ]
        
        for dx, dy, nombre in direcciones:
            nx, ny = self.x + dx, self.y + dy
            
            if entorno.es_posicion_valida(nx, ny):
                # Ejercicio 3: Verificar si hay obstáculo
                if entorno.hay_obstaculo(nx, ny):
                    self.obstaculos_conocidos.add((nx, ny))
                else:
                    percepcion['vecinos_validos'].append((nx, ny, nombre))
                    
                    # Ejercicio 1: Verificar si fue visitado
                    if self.con_memoria and (nx, ny) not in self.visitados:
                        percepcion['vecinos_no_visitados'].append((nx, ny, nombre))
        
        return percepcion
    
    def decidir(self, percepcion: Dict) -> str:
        """
        Decide la acción basándose en la percepción.
        
        Estrategia:
        1. Si hay suciedad aquí -> limpiar
        2. Si hay vecinos no visitados -> ir a uno
        3. Si todos visitados -> movimiento aleatorio
        
        Args:
            percepcion: Información del entorno
            
        Returns:
            Acción a ejecutar
        """
        # Prioridad 1: Limpiar si hay suciedad
        if percepcion['hay_suciedad']:
            return 'limpiar'
        
        # Prioridad 2: Explorar lugares no visitados
        if self.con_memoria and percepcion['vecinos_no_visitados']:
            _, _, direccion = random.choice(percepcion['vecinos_no_visitados'])
            return direccion
        
        # Prioridad 3: Movimiento aleatorio a vecinos válidos
        if percepcion['vecinos_validos']:
            _, _, direccion = random.choice(percepcion['vecinos_validos'])
            return direccion
        
        # Si no hay opciones, esperar
        return 'esperar'
    
    def actuar(self, accion: str, entorno: Any) -> None:
        """
        Ejecuta la acción en el entorno.
        
        Args:
            accion: Acción a ejecutar
            entorno: Entorno de limpieza
        """
        if accion == 'limpiar':
            # Limpiar y registrar
            info = entorno.limpiar(self.x, self.y)
            if info['limpiado']:
                self.suciedad_limpiada += 1
                self.puntos_totales += info['valor']
                self.acciones_limpieza += 1
                self.limpiados.add((self.x, self.y))
                
                # Ejercicio 2: Registrar tipo
                tipo = info['tipo']
                self.suciedad_por_tipo[tipo] = self.suciedad_por_tipo.get(tipo, 0) + 1
        
        elif accion in ['arriba', 'abajo', 'izquierda', 'derecha']:
            # Mover el agente
            dx, dy = {
                'arriba': (0, -1),
                'abajo': (0, 1),
                'izquierda': (-1, 0),
                'derecha': (1, 0)
            }[accion]
            
            nuevo_x, nuevo_y = self.x + dx, self.y + dy
            
            # Verificar que sea válido y sin obstáculos
            if (entorno.es_posicion_valida(nuevo_x, nuevo_y) and
                not entorno.hay_obstaculo(nuevo_x, nuevo_y)):
                self.x, self.y = nuevo_x, nuevo_y
                self.movimientos += 1
                
                # Ejercicio 1: Registrar visita
                if self.con_memoria:
                    self.visitados.add((self.x, self.y))
    
    def get_estadisticas(self) -> Dict:
        """Retorna estadísticas del agente."""
        return {
            'id': self.id,
            'posicion': (self.x, self.y),
            'suciedad_limpiada': self.suciedad_limpiada,
            'puntos_totales': self.puntos_totales,
            'movimientos': self.movimientos,
            'acciones_limpieza': self.acciones_limpieza,
            'lugares_visitados': len(self.visitados),
            'lugares_limpiados': len(self.limpiados),
            'obstaculos_conocidos': len(self.obstaculos_conocidos),
            'suciedad_por_tipo': self.suciedad_por_tipo.copy(),
            'eficiencia': (
                self.suciedad_limpiada / self.movimientos 
                if self.movimientos > 0 else 0
            )
        }

