# src/utils/pathfinding.py
from typing import List, Tuple, Optional, Dict, Any
from collections import deque
import math


def bfs(inicio: Tuple[int, int], objetivo: Tuple[int, int], 
        es_valido_func, hay_obstaculo_func, max_profundidad: int = 100) -> Optional[List[str]]:
    """
    Búsqueda en amplitud para encontrar camino entre inicio y objetivo
    
    Args:
        inicio: Posición inicial (x, y)
        objetivo: Posición objetivo (x, y)
        es_valido_func: Función que verifica si una posición es válida
        hay_obstaculo_func: Función que verifica si hay obstáculo
        max_profundidad: Profundidad máxima de búsqueda
    
    Returns:
        Lista de direcciones o None si no hay camino
    """
    if inicio == objetivo:
        return []
    
    cola = deque([(inicio[0], inicio[1], [])])
    visitados = {inicio}
    direcciones = [
        (0, -1, 'arriba'),
        (0, 1, 'abajo'),
        (-1, 0, 'izquierda'), 
        (1, 0, 'derecha')
    ]
    
    while cola and len(visitados) < max_profundidad:
        x, y, camino = cola.popleft()
        
        if (x, y) == objetivo:
            return camino
        
        for dx, dy, direccion in direcciones:
            nx, ny = x + dx, y + dy
            
            if ((nx, ny) not in visitados and 
                es_valido_func(nx, ny) and 
                not hay_obstaculo_func(nx, ny)):
                visitados.add((nx, ny))
                cola.append((nx, ny, camino + [direccion]))
    
    return None


def a_star(inicio: Tuple[int, int], objetivo: Tuple[int, int],
           es_valido_func, hay_obstaculo_func, 
           heuristica_func=None) -> Optional[List[str]]:
    """
    Algoritmo A* para encontrar el camino óptimo
    
    Args:
        inicio: Posición inicial (x, y)
        objetivo: Posición objetivo (x, y)
        es_valido_func: Función que verifica si una posición es válida
        hay_obstaculo_func: Función que verifica si hay obstáculo
        heuristica_func: Función heurística (por defecto distancia Manhattan)
    
    Returns:
        Lista de direcciones o None si no hay camino
    """
    if heuristica_func is None:
        heuristica_func = lambda a, b: abs(a[0]-b[0]) + abs(a[1]-b[1])
    
    open_set = {inicio}
    came_from = {}
    g_score = {inicio: 0}
    f_score = {inicio: heuristica_func(inicio, objetivo)}
    
    direcciones = [
        (0, -1, 'arriba'),
        (0, 1, 'abajo'),
        (-1, 0, 'izquierda'),
        (1, 0, 'derecha')
    ]
    
    while open_set:
        current = min(open_set, key=lambda pos: f_score.get(pos, float('inf')))
        
        if current == objetivo:
            # Reconstruir camino
            camino = []
            while current in came_from:
                current, direccion = came_from[current]
                camino.append(direccion)
            return camino[::-1]
        
        open_set.remove(current)
        
        for dx, dy, direccion in direcciones:
            neighbor = (current[0] + dx, current[1] + dy)
            
            # CORRECCIÓN: Cambiar "es_valida_func" por "es_valido_func"
            if not es_valido_func(neighbor[0], neighbor[1]) or hay_obstaculo_func(neighbor[0], neighbor[1]):
                continue
            
            tentative_g_score = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = (current, direccion)
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristica_func(neighbor, objetivo)
                if neighbor not in open_set:
                    open_set.add(neighbor)
    
    return None


def dijkstra(inicio: Tuple[int, int], objetivo: Tuple[int, int],
             es_valido_func, hay_obstaculo_func) -> Optional[List[str]]:
    """
    Algoritmo de Dijkstra para encontrar el camino más corto
    """
    from queue import PriorityQueue
    
    if inicio == objetivo:
        return []
    
    frontier = PriorityQueue()
    frontier.put((0, inicio))
    came_from = {inicio: None}
    cost_so_far = {inicio: 0}
    
    direcciones = [
        (0, -1, 'arriba'),
        (0, 1, 'abajo'),
        (-1, 0, 'izquierda'),
        (1, 0, 'derecha')
    ]
    
    while not frontier.empty():
        _, current = frontier.get()
        
        if current == objetivo:
            break
        
        for dx, dy, direccion in direcciones:
            neighbor = (current[0] + dx, current[1] + dy)
            
            if not es_valido_func(neighbor[0], neighbor[1]) or hay_obstaculo_func(neighbor[0], neighbor[1]):
                continue
            
            new_cost = cost_so_far[current] + 1
            
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost
                frontier.put((priority, neighbor))
                came_from[neighbor] = (current, direccion)
    
    # Reconstruir camino
    if objetivo not in came_from:
        return None
    
    current = objetivo
    path = []
    while current != inicio:
        current, direccion = came_from[current]
        path.append(direccion)
    
    return path[::-1]