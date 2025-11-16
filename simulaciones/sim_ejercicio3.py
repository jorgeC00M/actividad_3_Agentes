"""
Simulación Ejercicio 3: Agente que evita obstáculos fijos.
"""

import sys
sys.path.insert(0, '.')

from src.agentes.agente_limpieza import AgenteLimpieza
from src.entornos.entorno_limpieza import EntornoLimpieza
from src.utils.visualizacion import mostrar_grid, limpiar_pantalla
from src.config.parametros import CONFIG_LIMPIEZA, PASOS_SIMULACION
import time


def simular_ejercicio3():
    """Ejecuta la simulación del ejercicio 3."""
    print("\n" + "=" * 70)
    print("EJERCICIO 3: EVITACIÓN DE OBSTÁCULOS")
    print("=" * 70)
    print("\nCaracterísticas:")
    print("  ✓ Obstáculos fijos (🧱) que el agente debe evitar")
    print("  ✓ El agente aprende dónde están los obstáculos")
    print("  ✓ Navega inteligentemente alrededor de ellos")
    
    # Crear entorno con obstáculos
    entorno = EntornoLimpieza(
        ancho=CONFIG_LIMPIEZA['ancho'],
        alto=CONFIG_LIMPIEZA['alto'],
        num_suciedad=CONFIG_LIMPIEZA['num_suciedad'],
        num_obstaculos=CONFIG_LIMPIEZA['num_obstaculos'],  # Con obstáculos
        tipos_suciedad=True
    )
    
    # Crear agente
    agente = AgenteLimpieza(x=0, y=0, con_memoria=True)
    
    print(f"\nConfiguración:")
    print(f"  - Grid: {entorno.ancho}x{entorno.alto}")
    print(f"  - Suciedad: {entorno.get_suciedad_restante()}")
    print(f"  - Obstáculos: {len(entorno.obstaculos)}")
    
    input("\nPresiona Enter para comenzar...")
    
    # Simulación
    for paso in range(PASOS_SIMULACION):
        agente.update(entorno)
        
        # Mostrar cada 5 pasos
        if paso % 5 == 0 or entorno.get_suciedad_restante() == 0:
            limpiar_pantalla()
            
            stats = agente.get_estadisticas()
            mostrar_grid(
                entorno,
                [agente],
                f"EJERCICIO 3 - Paso {paso + 1}/{PASOS_SIMULACION}",
                {
                    'Suciedad limpiada': stats['suciedad_limpiada'],
                    'Puntos': stats['puntos_totales'],
                    'Obstáculos conocidos': stats['obstaculos_conocidos'],
                    'Eficiencia': f"{stats['eficiencia']:.2%}"
                }
            )
            time.sleep(0.5)
        
        if entorno.get_suciedad_restante() == 0:
            print("\n✅ ¡Toda la suciedad ha sido limpiada!")
            break
    
    print("\n" + "=" * 70)
    print(f"Obstáculos detectados: {agente.get_estadisticas()['obstaculos_conocidos']}")
    print("=" * 70)


if __name__ == "__main__":
    simular_ejercicio3()