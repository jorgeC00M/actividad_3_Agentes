"""
Simulación Ejercicio 4: Comunicación entre agentes recolectores.
"""

import sys
sys.path.insert(0, '.')

from src.agentes.agente_recolector import AgenteRecolector
from src.entornos.entorno_recoleccion import EntornoRecoleccion
from src.utils.visualizacion import mostrar_grid, limpiar_pantalla
from src.config.parametros import CONFIG_RECOLECCION, PASOS_SIMULACION
import time


def simular_ejercicio4():
    """Ejecuta la simulación del ejercicio 4."""
    print("\n" + "=" * 70)
    print("EJERCICIO 4: COMUNICACIÓN ENTRE AGENTES")
    print("=" * 70)
    print("\nCaracterísticas:")
    print("  ✓ Múltiples agentes cooperan")
    print("  ✓ Comparten información sobre objetivos")
    print("  ✓ Evitan ir al mismo recurso")
    
    # Crear entorno
    entorno = EntornoRecoleccion(
        ancho=CONFIG_RECOLECCION['ancho'],
        alto=CONFIG_RECOLECCION['alto'],
        num_comida=CONFIG_RECOLECCION['num_comida'],
        competitivo=False
    )
    
    # Crear agentes cooperativos
    agentes = []
    posiciones_inicio = [(0, 0), (14, 0), (0, 14)]
    
    for i, (x, y) in enumerate(posiciones_inicio[:CONFIG_RECOLECCION['num_agentes']]):
        agente = AgenteRecolector(
            x=x, y=y,
            modo='cooperativo',
            con_aprendizaje=False
        )
        agentes.append(agente)
        entorno.agregar_agente(agente)
    
    print(f"\nConfiguración:")
    print(f"  - Grid: {entorno.ancho}x{entorno.alto}")
    print(f"  - Comida inicial: {entorno.get_comida_restante()}")
    print(f"  - Agentes: {len(agentes)}")
    
    input("\nPresiona Enter para comenzar...")
    
    # Simulación
    for paso in range(PASOS_SIMULACION):
        # Actualizar cada agente
        for agente in agentes:
            agente.update(entorno)
            
            # Comunicar objetivo a otros
            if agente.objetivo_actual:
                agente.enviar_mensaje(
                    [a for a in agentes if a.id != agente.id],
                    'objetivo_reclamado',
                    agente.objetivo_actual
                )
        
        # Avanzar entorno
        entorno.step()
        
        # Mostrar cada 5 pasos
        if paso % 5 == 0 or entorno.get_comida_restante() == 0:
            limpiar_pantalla()
            
            stats_totales = {
                'Comida restante': entorno.get_comida_restante(),
                'Total recolectado': sum(a.comida_recolectada for a in agentes)
            }
            
            mostrar_grid(
                entorno,
                agentes,
                f"EJERCICIO 4 - Paso {paso + 1}/{PASOS_SIMULACION}",
                stats_totales
            )
            
            print("Agentes:")
            for agente in agentes:
                stats = agente.get_estadisticas()
                print(f"  {agente.id}: {stats['comida_recolectada']} comida, "
                      f"energía: {stats['energia']}")
            
            time.sleep(0.5)
        
        if entorno.get_comida_restante() == 0:
            print("\n✅ ¡Toda la comida ha sido recolectada!")
            break
    
    # Estadísticas finales
    print("\n" + "=" * 70)
    print("ESTADÍSTICAS FINALES")
    print("=" * 70)
    
    for agente in agentes:
        print(f"\n{agente.id}:")
        stats = agente.get_estadisticas()
        for clave, valor in stats.items():
            print(f"  {clave}: {valor}")


if __name__ == "__main__":
    simular_ejercicio4()
