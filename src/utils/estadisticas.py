"""Utilidades para cálculo de estadísticas."""

from typing import List, Dict, Any


def calcular_estadisticas_globales(agentes: List[Any]) -> Dict:
    """
    Calcula estadísticas globales de todos los agentes.
    
    Args:
        agentes: Lista de agentes
        
    Returns:
        Dict con estadísticas globales
    """
    if not agentes:
        return {}
    
    stats = {
        'num_agentes': len(agentes),
        'total_recursos': 0,
        'promedio_recursos': 0,
        'agente_mas_exitoso': None,
        'max_recursos': 0
    }
    
    for agente in agentes:
        stats_agente = agente.get_estadisticas()
        
        # Sumar recursos (puede ser comida o suciedad según el tipo)
        recursos = stats_agente.get('comida_recolectada', 0) or stats_agente.get('suciedad_limpiada', 0)
        stats['total_recursos'] += recursos
        
        if recursos > stats['max_recursos']:
            stats['max_recursos'] = recursos
            stats['agente_mas_exitoso'] = agente.id
    
    if len(agentes) > 0:
        stats['promedio_recursos'] = stats['total_recursos'] / len(agentes)
    
    return stats