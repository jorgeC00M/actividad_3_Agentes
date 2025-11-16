"""
Simulación Ejercicio 5: Agente con memoria espacial (aprendizaje).
"""

import sys
sys.path.insert(0, '.')

from src.agentes.agente_recolector import AgenteRecolector
from src.entornos.entorno_recoleccion import EntornoRecoleccion
from src.utils.visualizacion import mostrar_grid, limpiar_pantalla
import time


def simular_ejercicio5():
    """Ejecuta la simulación del ejercicio 5."""
    print("\n" + "=" * 70)
    print("EJERCICIO 5: MEMORIA ESPACIAL Y APRENDIZAJE")
    print("=" * 70)
    print("\nCaracterísticas:")
    print("  ✓ El agente aprende qué áreas tienen más comida")
    print("  ✓ Mantiene un mapa de calor de recursos")
    print("  ✓ Prioriza zonas con mayor probabilidad de comida")
    
    # Crear entorno
    entorno = EntornoRecoleccion(ancho=15, alto=15, num_comida=25)
    
    # Crear agente con aprendizaje
    agente = AgenteRecolector(
        x=7, y=7,
        modo='cooperativo',
        con_aprendizaje=True  # Activar aprendizaje
    )
    entorno.agregar_agente(agente)
    
    print(f"\nConfiguración:")
    print(f"  - Grid: {entorno.ancho}x{entorno.alto}")
    print(f"  - Comida inicial: {entorno.get_comida_restante()}")
    print(f"  - Aprendizaje: Activado")
    
    input("\nPresiona Enter para comenzar...")
    
    # Simulación en fases
    FASES = 2
    PASOS_POR_FASE = 30
    
    for fase in range(FASES):
        print(f"\n--- FASE {fase + 1} ---")
        
        # Resetear entorno pero mantener memoria del agente
        entorno.reset()
        agente.x, agente.y = 7, 7
        agente.comida_recolectada = 0
        agente.energia = 100
        
        for paso in range(PASOS_POR_FASE):
            agente.update(entorno)
            entorno.step()
            
            # Mostrar cada 5 pasos
            if paso % 5 == 0:
                limpiar_pantalla()
                
                stats = agente.get_estadisticas()
                mostrar_grid(
                    entorno,
                    [agente],
                    f"EJERCICIO 5 - Fase {fase + 1} - Paso {paso + 1}/{PASOS_POR_FASE}",
                    {
                        'Comida recolectada': stats['comida_recolectada'],
                        'Energía': stats['energia'],
                        'Zonas aprendidas': stats['zonas_aprendidas'],
                        'Comida restante': entorno.get_comida_restante()
                    }
                )
                
                time.sleep(0.5)
            
            if agente.energia <= 0:
                print("\n⚠️  Agente sin energía")
                break
        
        print(f"\nFase {fase + 1} completada")
        print(f"  - Comida recolectada: {agente.comida_recolectada}")
        print(f"  - Zonas mapeadas: {len(agente.mapa_calor)}")
        
        if fase < FASES - 1:
            input("\nPresiona Enter para la siguiente fase...")
    
    # Mostrar mapa de calor aprendido
    print("\n" + "=" * 70)
    print("MAPA DE CALOR APRENDIDO (Top 10 zonas)")
    print("=" * 70)
    
    zonas_ordenadas = sorted(
        agente.mapa_calor.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    for pos, valor in zonas_ordenadas:
        print(f"  Posición {pos}: {valor} puntos")


if __name__ == "__main__":
    simular_ejercicio5()