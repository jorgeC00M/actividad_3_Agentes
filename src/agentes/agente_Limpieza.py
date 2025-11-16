"""
Agentes de limpieza - Ejercicios 1, 2 y 3
"""

import random
from typing import Set, Dict, Any
from .agente_base import AgenteBase


class AgenteLimpiezaBase(AgenteBase):
    """Agente limpiador básico (código original)"""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.suciedad_limpiada = 0
    
    def percibir(self, entorno):
        return entorno.hay_suciedad(self.x, self.y)
    
    def decidir(self, percepcion):
        if percepcion:
            return "limpiar"
        else:
            return random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
    
    def actuar(self, decision, entorno):
        if decision == "limpiar":
            if entorno.limpiar(self.x, self.y):
                self.suciedad_limpiada += 1
        else:
            self.mover(decision, entorno)


class AgenteLimpiezaConMemoria(AgenteLimpiezaBase):
    """Ejercicio 1: Agente que recuerda lugares visitados"""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.lugares_visitados: Set[tuple] = set()
        self.ultima_direccion = None
    
    def decidir(self, percepcion):
        # Registrar posición actual
        self.lugares_visitados.add((self.x, self.y))
        
        if percepcion:
            return "limpiar"
        else:
            # Priorizar direcciones no visitadas
            direcciones_no_visitadas = []
            for dx, dy, direccion in [(0, -1, 'arriba'), (0, 1, 'abajo'), 
                                    (-1, 0, 'izquierda'), (1, 0, 'derecha')]:
                nx, ny = self.x + dx, self.y + dy
                if (nx, ny) not in self.lugares_visitados:
                    direcciones_no_visitadas.append(direccion)
            
            if direcciones_no_visitadas:
                self.ultima_direccion = random.choice(direcciones_no_visitadas)
            else:
                self.ultima_direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
            
            return self.ultima_direccion


class AgenteLimpiezaConTipos(AgenteLimpiezaBase):
    """Ejercicio 2: Agente que maneja diferentes tipos de suciedad"""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.tipos_limpiados: Dict[str, int] = {}
        self.puntos_totales = 0
    
    def decidir(self, percepcion):
        if percepcion:
            return "limpiar"
        else:
            return random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
    
    def actuar(self, decision, entorno):
        if decision == "limpiar":
            resultado = entorno.limpiar(self.x, self.y)
            if resultado:
                tipo, puntos = resultado
                self.suciedad_limpiada += 1
                self.tipos_limpiados[tipo] = self.tipos_limpiados.get(tipo, 0) + 1
                self.puntos_totales += puntos
        else:
            self.mover(decision, entorno)


class AgenteLimpiezaConEvasion(AgenteLimpiezaBase):
    """Ejercicio 3: Agente que evita obstáculos"""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.obstaculos_detectados: Set[tuple] = set()
    
    def percibir(self, entorno):
        # Detectar obstáculos cercanos
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                nx, ny = self.x + dx, self.y + dy
                if entorno.es_valida(nx, ny) and entorno.hay_obstaculo(nx, ny):
                    self.obstaculos_detectados.add((nx, ny))
        
        return super().percibir(entorno)
    
    def decidir(self, percepcion):
        if percepcion:
            return "limpiar"
        else:
            # Filtrar direcciones seguras (sin obstáculos)
            direcciones_seguras = []
            for dx, dy, direccion in [(0, -1, 'arriba'), (0, 1, 'abajo'), 
                                    (-1, 0, 'izquierda'), (1, 0, 'derecha')]:
                nx, ny = self.x + dx, self.y + dy
                if (nx, ny) not in self.obstaculos_detectados:
                    direcciones_seguras.append(direccion)
            
            if direcciones_seguras:
                return random.choice(direcciones_seguras)
            else:
                return "esperar"  # No moverse si no hay direcciones seguras