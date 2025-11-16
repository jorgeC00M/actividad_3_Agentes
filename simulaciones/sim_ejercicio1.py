"""
Simulación Ejercicio 1: Agente limpiador con memoria de lugares visitados.
"""

import sys
sys.path.insert(0, '.')

from src.agentes.agente_limpieza import AgenteLimpieza
from src.entornos.entorno_limpieza import EntornoLimpieza
from src.utils.visualizacion import mostrar_grid, limpiar_pantalla
from src.config.parametros import CONFIG_LIMPIEZA, PASOS_SIMULACION
import time


def simular_ejercicio1():
    """Ejecuta la simulación del ejercicio 1."""
    print("\n" + "=" * 70)
    print("EJERCICIO 1: AGENTE LIMPIADOR CON MEMORIA")
    print("=" * 70)
    print("\nCaracterísticas:")
    print("  ✓ El agente recuerda lugares visitados")
    print("  ✓ Prioriza explorar áreas no visitadas")
    print("  ✓ Evita recorrer el mismo lugar innecesariamente")
    
    # Crear entorno
    entorno = EntornoLimpieza(
        ancho=CONFIG_LIMPIEZA['ancho'],
        alto=CONFIG_LIMPIEZA['alto'],
        num_suciedad=CONFIG_LIMPIEZA['num_suciedad'],
        num_obstaculos=0,  # Sin obstáculos en ejercicio 1
        tipos_suciedad=False  # Sin tipos en ejercicio 1
    )
    
    # Crear agente con memoria
    agente = AgenteLimpieza(x=0, y=0, con_memoria=True)
    
    print(f"\nConfiguración:")
    print(f"  - Grid: {entorno.ancho}x{entorno.alto}")
    print(f"  - Suciedad inicial: {entorno.get_suciedad_restante()}")
    print(f"  - Agente: {agente.id}")
    
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
                f"EJERCICIO 1 - Paso {paso + 1}/{PASOS_SIMULACION}",
                {
                    'Suciedad limpiada': stats['suciedad_limpiada'],
                    'Suciedad restante': entorno.get_suciedad_restante(),
                    'Lugares visitados': stats['lugares_visitados'],
                    'Movimientos': stats['movimientos'],
                    'Eficiencia': f"{stats['eficiencia']:.2%}"
                }
            )
            time.sleep(0.5)
        
        # Terminar si limpió todo
        if entorno.get_suciedad_restante() == 0:
            print("\n✅ ¡Toda la suciedad ha sido limpiada!")
            break
    
    # Estadísticas finales
    print("\n" + "=" * 70)
    print("ESTADÍSTICAS FINALES")
    print("=" * 70)
    
    stats_finales = agente.get_estadisticas()
    for clave, valor in stats_finales.items():
        if isinstance(valor, float):
            print(f"{clave}: {valor:.2f}")
        elif isinstance(valor, dict):
            print(f"{clave}: {valor}")
        else:
            print(f"{clave}: {valor}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    simular_ejercicio1()
