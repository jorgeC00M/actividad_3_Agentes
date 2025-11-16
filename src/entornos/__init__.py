# Paquete de entornos (mundos donde viven los agentes).
"""Módulo de entornos."""

from .entorno_base import EntornoBase
from .entorno_limpieza import EntornoLimpieza
from .entorno_recoleccion import EntornoRecoleccion

__all__ = ['EntornoBase', 'EntornoLimpieza', 'EntornoRecoleccion']