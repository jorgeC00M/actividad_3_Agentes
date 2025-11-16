"""
Módulo de agentes - Implementaciones de diferentes tipos de agentes
"""

from .agente_base import AgenteBase
from .agente_limpieza import (
    AgenteLimpiezaBase,
    AgenteLimpiezaConMemoria,
    AgenteLimpiezaConTipos,
    AgenteLimpiezaConEvasion
)
from .agente_recolector import (
    AgenteRecolectorBase,
    AgenteRecolectorComunicativo,
    AgenteRecolectorConAprendizaje,
    AgenteCompetitivo
)

__all__ = [
    'AgenteBase',
    'AgenteLimpiezaBase',
    'AgenteLimpiezaConMemoria',
    'AgenteLimpiezaConTipos',
    'AgenteLimpiezaConEvasion',
    'AgenteRecolectorBase',
    'AgenteRecolectorComunicativo',
    'AgenteRecolectorConAprendizaje',
    'AgenteCompetitivo'
]