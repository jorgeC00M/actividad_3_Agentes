# src/entornos/entorno_base.py
from abc import ABC, abstractmethod
from typing import List, Set, Dict, Any, Tuple


class EntornoBase(ABC):
    """Clase base abstracta para todos los entornos"""
    
    def __init__(self, ancho: int, alto: int):
        self.ancho = ancho
        self.alto = alto
        self.agentes = []
        self.tiempo = 0
    
    def es_valida(self, x: int, y: int) -> bool:
        """Verifica si una posición está dentro del grid"""
        return 0 <= x < self.ancho and 0 <= y < self.alto
    
    def agregar_agente(self, agente):
        """Añade un agente al entorno"""
        if self.es_valida(agente.x, agente.y):
            self.agentes.append(agente)
            return True
        return False
    
    def remover_agente(self, agente):
        """Remueve un agente del entorno"""
        if agente in self.agentes:
            self.agentes.remove(agente)
            return True
        return False
    
    @abstractmethod
    def actualizar(self):
        """Actualiza el estado del entorno"""
        pass
    
    def ejecutar_paso(self):
        """Ejecuta un paso de simulación para todos los agentes"""
        agentes_activos = []
        
        for agente in self.agentes[:]:  # Copia para poder remover
            if agente.ciclo_vida(self):
                agentes_activos.append(agente)
            else:
                self.remover_agente(agente)
        
        self.actualizar()
        self.tiempo += 1
        
        return {
            'tiempo': self.tiempo,
            'agentes_activos': len(agentes_activos),
            'agentes_totales': len(self.agentes)
        }
    
    def __str__(self):
        return f"{self.__class__.__name__}({self.ancho}x{self.alto})"