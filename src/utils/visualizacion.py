"""
Utilidades de visualización para los entornos
"""

from typing import List
import sys


class Visualizador:
    """Clase para visualizar entornos en consola"""
    
    @staticmethod
    def mostrar_entorno_limpieza(entorno, agente=None):
        """Muestra el entorno de limpieza en consola"""
        print(f"Tiempo: {entorno.tiempo} | Suciedad: {len(entorno.suciedad)}")
        
        for y in range(entorno.alto):
            for x in range(entorno.ancho):
                if agente and x == agente.x and y == agente.y:
                    print("A", end=" ")
                elif hasattr(entorno, 'obstaculos') and (x, y) in entorno.obstaculos:
                    print("X", end=" ")
                elif hasattr(entorno, 'suciedad'):
                    if isinstance(entorno.suciedad, dict) and (x, y) in entorno.suciedad:
                        tipo = entorno.suciedad[(x, y)]['tipo']
                        print(entorno.tipos_suciedad[tipo]['simbolo'], end=" ")
                    elif (x, y) in entorno.suciedad:
                        print("*", end=" ")
                    else:
                        print(".", end=" ")
                else:
                    print(".", end=" ")
            print()
        print()
    
    @staticmethod
    def mostrar_entorno_recoleccion(entorno, agentes=None):
        """Muestra el entorno de recolección en consola"""
        if agentes is None:
            agentes = []
            
        print(f"Tiempo: {entorno.tiempo} | Comida: {len(entorno.comida)}")
        
        for y in range(entorno.alto):
            for x in range(entorno.ancho):
                # Verificar agentes primero
                agente_en_pos = None
                for agente in agentes:
                    if agente.x == x and agente.y == y:
                        agente_en_pos = agente
                        break
                
                if agente_en_pos:
                    print(agente_en_pos.id[0] if hasattr(agente_en_pos, 'id') else "A", end=" ")
                elif (x, y) in entorno.obstaculos:
                    print("X", end=" ")
                elif (x, y) in entorno.comida:
                    print("C", end=" ")
                else:
                    print(".", end=" ")
            print()
        print()
    
    @staticmethod
    def mostrar_estadisticas_agente(agente):
        """Muestra estadísticas de un agente"""
        print(f"Agente: {agente}")
        print(f"Posición: ({agente.x}, {agente.y})")
        print(f"Energía: {agente.energia}")
        
        if hasattr(agente, 'suciedad_limpiada'):
            print(f"Suciedad limpiada: {agente.suciedad_limpiada}")
        
        if hasattr(agente, 'comida_recolectada'):
            print(f"Comida recolectada: {agente.comida_recolectada}")
        
        if hasattr(agente, 'puntos_totales'):
            print(f"Puntos totales: {agente.puntos_totales}")
        
        if hasattr(agente, 'tipos_limpiados'):
            print(f"Tipos limpiados: {agente.tipos_limpiados}")
        
        if hasattr(agente, 'lugares_visitados'):
            print(f"Lugares visitados: {len(agente.lugares_visitados)}")
        
        print()
    
    @staticmethod
    def limpiar_consola():
        """Limpia la consola (funciona en Windows y Unix)"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')