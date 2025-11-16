"""
Simulación Ejercicio 2: Diferentes tipos de suciedad con distintos valores.
"""

import sys
sys.path.insert(0, '.')

from src.agentes.agente_limpieza import AgenteLimpieza
from src.entornos.entorno_limpieza import EntornoLimpieza
from src.utils.visualizacion import mostrar_grid, limpiar_pantalla
from src.config.parametros import CONFIG_LIMPIEZA, PASOS_SIMULACION
import time


def simular_ejercicio2():
    """Ejecuta la simulación del ejercicio 2."""
    print("\n" + "=" * 70)
    print("EJERCICIO 2: TIPOS DE SUCIEDAD CON DIFERENTES VALORES")
    print("=" * 70)
    print("\nTipos de suciedad:")
    print("  💨 Polvo: 1 punto")
    print("  💩 Mugre: 3 puntos")
    print("  🗑️  Basura: 5 puntos")
    
    # Crear entorno con tipos de suciedad
    entorno = EntornoLimpieza(
        ancho=CONFIG_LIMPIEZA['ancho'],
        alto=CONFIG_LIMPIEZA['alto'],
        num_suciedad=CONFIG_LIMPIEZA['num_suciedad'],
        num_obstaculos=0,
        tipos_suciedad=True  # Activar tipos de suciedad
    )
    
    # Crear agente
    agente = AgenteLimpieza(x=0, y=0, con_memoria=True)
    
    print(f"\nConfiguración:")
    print(f"  - Grid: {entorno.ancho}x{entorno.alto}")
    print(f"  - Suciedad total: {entorno.get_suciedad_restante()}")
    
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
                f"EJERCICIO 2 - Paso {paso + 1}/{PASOS_SIMULACION}",
                {
                    'Suciedad limpiada': stats['suciedad_limpiada'],
                    'Puntos totales': stats['puntos_totales'],
                    'Suciedad restante': entorno.get_suciedad_restante(),
                    'Por tipo': str(stats['suciedad_por_tipo'])
                }
            )
            time.sleep(0.5)
        
        if entorno.get_suciedad_restante() == 0:
            print("\n✅ ¡Toda la suciedad ha sido limpiada!")
            break
    
    # Estadísticas finales
    print("\n" + "=" * 70)
    print("ESTADÍSTICAS FINALES")
    print("=" * 70)
    
    stats_finales = agente.get_estadisticas()
    print(f"\nSuciedad limpiada por tipo:")
    for tipo, cantidad in stats_finales['suciedad_por_tipo'].items():
        print(f"  {tipo}: {cantidad}")
    
    print(f"\nPuntos totales: {stats_finales['puntos_totales']}")
    print(f"Eficiencia: {stats_finales['eficiencia']:.2%}")


if __name__ == "__main__":
    simular_ejercicio2()