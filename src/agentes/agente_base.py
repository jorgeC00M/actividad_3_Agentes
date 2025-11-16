"""Clase base para todos los agentes."""

from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple
import uuid


class AgenteBase(ABC):
    """
    Clase base abstracta para todos los agentes.
    
    Implementa el patrón Template Method para el ciclo del agente:
    percibir -> decidir -> actuar
    """
    
    def __init__(self, id_agente: Optional[str] = None, x: int = 0, y: int = 0):
        """
        Inicializa el agente base.
        
        Args:
            id_agente: Identificador único del agente
            x: Posición inicial en x
            y: Posición inicial en y
        """
        self.id = id_agente or str(uuid.uuid4())[:8]
        self.x = x
        self.y = y
        self.activo = True
        self.pasos = 0
    
    @abstractmethod
    def percibir(self, entorno: Any) -> Any:
        """
        Percibe el entorno y retorna la información relevante.
        
        Args:
            entorno: Entorno donde opera el agente
            
        Returns:
            Información percibida del entorno
        """
        pass
    
    @abstractmethod
    def decidir(self, percepcion: Any) -> Any:
        """
        Decide qué acción tomar basándose en la percepción.
        
        Args:
            percepcion: Información percibida del entorno
            
        Returns:
            Acción a ejecutar
        """
        pass
    
    @abstractmethod
    def actuar(self, accion: Any, entorno: Any) -> None:
        """
        Ejecuta la acción en el entorno.
        
        Args:
            accion: Acción a ejecutar
            entorno: Entorno donde ejecutar la acción
        """
        pass
    
    def update(self, entorno: Any) -> None:
        """
        Ciclo completo del agente: percibir -> decidir -> actuar.
        
        Args:
            entorno: Entorno donde opera el agente
        """
        if not self.activo:
            return
        
        percepcion = self.percibir(entorno)
        accion = self.decidir(percepcion)
        self.actuar(accion, entorno)
        self.pasos += 1
    
    def get_posicion(self) -> Tuple[int, int]:
        """Retorna la posición actual del agente."""
        return (self.x, self.y)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, pos=({self.x},{self.y}))"
