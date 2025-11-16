"""Algoritmos de búsqueda de caminos."""

from typing import List, Tuple, Set, Optional
from collections import deque


def bfs_camino(
    inicio: Tuple[int, int],
    objetivo: Tuple[int, int],
    es_valido_fn,
    ancho: int,
    alto: int
) -> List[str]:
    """
    Búsqueda en anchura (BFS) para encontrar camino.
    
    Args:
        inicio: Posición inicial
        objetivo: Posición objetivo
        es_valido_fn: Función que verifica si una posición es válida
        ancho: Ancho del grid
        alto: Alto del grid
        
    Returns:
        Lista de direcciones o lista vacía si no hay camino
    """
    cola = deque([(inicio[0], inicio[1], [])])
    visitados: Set[Tuple[int, int]] = {inicio}
    
    direcciones = [
        (0, -1, 'arriba'),
        (0, 1, 'abajo'),
        (-1, 0, 'izquierda'),
        (1, 0, 'derecha')
    ]
    
    while cola:
        x, y, camino = cola.popleft()
        
        if (x, y) == objetivo:
            return camino
        
        for dx, dy, nombre in direcciones:
            nx, ny = x + dx, y + dy
            
            if (0 <= nx < ancho and 0 <= ny < alto and
                (nx, ny) not in visitados and
                es_valido_fn(nx, ny)):
                
                visitados.add((nx, ny))
                cola.append((nx, ny, camino + [nombre]))
    
    return []
