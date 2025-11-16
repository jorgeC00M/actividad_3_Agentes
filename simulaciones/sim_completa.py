# simulaciones/sim_completa.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agentes.agente_Limpieza import (
    AgenteLimpiezaConMemoria, 
    AgenteLimpiezaConTipos, 
    AgenteLimpiezaConEvasion
)
from src.agentes.agente_recolector import (
    AgenteRecolectorComunicativo,
    AgenteRecolectorConAprendizaje, 
    AgenteCompetitivo
)
from src.entornos.entorno_limpieza import (
    EntornoLimpieza,
    EntornoLimpiezaConTipos,
    EntornoLimpiezaConObstaculos
)
from src.entornos.entorno_recoleccion import (
    EntornoRecoleccion,
    EntornoRecoleccionCompetitivo
)
from src.utils.visualizacion import Visualizador


def demo_rapida_ejercicios():
    """Demostración rápida de todos los ejercicios"""
    print("=== DEMOSTRACIÓN COMPLETA - TODOS LOS EJERCICIOS ===\n")
    
    # Ejercicio 1 - Memoria
    print("1. EJERCICIO 1 - Agente con memoria")
    entorno1 = EntornoLimpieza(4, 4, 5)
    agente1 = AgenteLimpiezaConMemoria(2, 2)
    entorno1.agregar_agente(agente1)
    
    for _ in range(10):
        entorno1.ejecutar_paso()
    
    print(f"   Lugares visitados: {len(agente1.lugares_visitados)}")
    print(f"   Suciedad limpiada: {agente1.suciedad_limpiada}")
    print()
    
    # Ejercicio 2 - Tipos de suciedad
    print("2. EJERCICIO 2 - Tipos de suciedad")
    entorno2 = EntornoLimpiezaConTipos(4, 4, 6)
    agente2 = AgenteLimpiezaConTipos(1, 1)
    entorno2.agregar_agente(agente2)
    
    for _ in range(8):
        entorno2.ejecutar_paso()
    
    print(f"   Puntos totales: {agente2.puntos_totales}")
    print(f"   Tipos limpiados: {agente2.tipos_limpiados}")
    print()
    
    # Ejercicio 3 - Evasión de obstáculos
    print("3. EJERCICIO 3 - Evasión de obstáculos")
    entorno3 = EntornoLimpiezaConObstaculos(5, 5, 6, 4)
    agente3 = AgenteLimpiezaConEvasion(2, 2)
    entorno3.agregar_agente(agente3)
    
    for _ in range(8):
        entorno3.ejecutar_paso()
    
    print(f"   Obstáculos detectados: {len(agente3.obstaculos_detectados)}")
    print(f"   Energía restante: {agente3.energia}")
    print()
    
    # Ejercicio 4 - Comunicación
    print("4. EJERCICIO 4 - Comunicación entre agentes")
    entorno4 = EntornoRecoleccion(6, 6, 8, 3)
    agente4a = AgenteRecolectorComunicativo(0, 0, "A1")
    agente4b = AgenteRecolectorComunicativo(5, 5, "A2")
    entorno4.agregar_agente(agente4a)
    entorno4.agregar_agente(agente4b)
    
    for _ in range(12):
        entorno4.ejecutar_paso()
    
    print(f"   Comida total recolectada: {agente4a.comida_recolectada + agente4b.comida_recolectada}")
    print()
    
    # Ejercicio 5 - Aprendizaje
    print("5. EJERCICIO 5 - Memoria espacial")
    entorno5 = EntornoRecoleccion(5, 5, 6, 2)
    agente5 = AgenteRecolectorConAprendizaje(2, 2, "Aprendiz")
    entorno5.agregar_agente(agente5)
    
    for _ in range(15):
        entorno5.ejecutar_paso()
    
    print(f"   Áreas productivas: {len(agente5.areas_productivas)}")
    print(f"   Posiciones en memoria: {len(agente5.memoria_comida)}")
    print()
    
    # Ejercicio 6 - Competencia
    print("6. EJERCICIO 6 - Competencia por recursos")
    entorno6 = EntornoRecoleccionCompetitivo(6, 6, 4, 3)
    agente6a = AgenteCompetitivo(0, 0, "A1", "agresiva")
    agente6b = AgenteCompetitivo(5, 5, "C1", "conservadora")
    entorno6.agregar_agente(agente6a)
    entorno6.agregar_agente(agente6b)
    
    for _ in range(20):
        entorno6.ejecutar_paso()
    
    print(f"   Ganador: {max([agente6a, agente6b], key=lambda a: a.comida_recolectada).id}")
    print(f"   Puntuaciones - A1: {agente6a.comida_recolectada}, C1: {agente6b.comida_recolectada}")
    
    print("\n" + "="*50)
    print("DEMOSTRACIÓN COMPLETADA")
    print("Para simulaciones completas, ejecute los archivos individuales.")


if __name__ == "__main__":
    demo_rapida_ejercicios()