# src/agentes/afente_base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple
import random


class AgenteBase(ABC):
    """Clase base abstracta para todos los agentes del sistema"""
    
    def __init__(self, x: int, y: int, agent_id: str = None):
        self.x = x
        self.y = y
        self.id = agent_id or f"agente_{id(self)}"
        self.energia = 100
        self.activo = True
        
    @abstractmethod
    def percibir(self, entorno) -> Any:
        """Recibe información del entorno"""
        pass
    
    @abstractmethod
    def decidir(self, percepcion: Any) -> str:
        """Toma una decisión basada en la percepción"""
        pass
    
    @abstractmethod
    def actuar(self, decision: str, entorno):
        """Ejecuta una acción en el entorno"""
        pass
    
    def ciclo_vida(self, entorno):
        """Ejecuta el ciclo completo de percepción-decisión-acción"""
        if not self.activo or self.energia <= 0:
            return False
            
        percepcion = self.percibir(entorno)
        decision = self.decidir(percepcion)
        self.actuar(decision, entorno)
        return True
    
    def mover(self, direccion: str, entorno) -> bool:
        """Intenta mover el agente en una dirección"""
        direcciones = {
            'arriba': (0, -1),
            'abajo': (0, 1),
            'izquierda': (-1, 0),
            'derecha': (1, 0)
        }
        
        if direccion in direcciones:
            dx, dy = direcciones[direccion]
            nuevo_x, nuevo_y = self.x + dx, self.y + dy
            
            if entorno.es_valida(nuevo_x, nuevo_y):
                self.x, self.y = nuevo_x, nuevo_y
                self.energia -= 1
                return True
        return False
    
    def __str__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"