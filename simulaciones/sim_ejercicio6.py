"""
Simulación Ejercicio 6: Sistema competitivo por recursos limitados.
"""

import sys
sys.path.insert(0, '.')

from src.agentes.agente_recolector import AgenteRecolector
from src.entornos.entorno_recoleccion import EntornoRecoleccion
from src.utils.visualizacion import mostrar_grid, limpiar_pantalla
from src.config.parametros import CONFIG_COMPETITIVO, PASOS_SIMULACION
import time


def simular_ejercicio6():
    """Ejecuta la simulación del ejercicio 6."""
    print("\n" + "=" * 70)
    print("EJERCICIO 6: SISTEMA COMPETITIVO")
    print("=" * 70)
    print("\nCaracterísticas:")
    print("  ✓ Múltiples agentes compiten por recursos limitados")
    print("  ✓ No hay comunicación cooperativa")
    print("  ✓ Cada agente busca maximizar su propio beneficio")
    print("  ✓ Los recursos se regeneran lentamente")
    
    # Crear entorno competitivo
    entorno = EntornoRecoleccion(
        ancho=CONFIG_COMPETITIVO['ancho'],
        alto=CONFIG_COMPETITIVO['alto'],
        num_comida=CONFIG_COMPETITIVO['num_comida'],
        competitivo=True  # Modo competitivo
    )
    
    # Crear agentes competitivos
    agentes = []
    posiciones = [
        (0, 0), (11, 0), (0, 11), (11, 11)
    ]
    
    colores_ids = ['🔴', '🔵', '🟢', '🟡']
    
    for i in range(CONFIG_COMPETITIVO['num_agentes']):
        x, y = posiciones[i]
        agente = AgenteRecolector(
            x=x, y=y,
            modo='competitivo',  # Modo competitivo
            con_aprendizaje=True
        )
        agente.id = f"{colores_ids[i]}-{agente.id[:4]}"
        agentes.append(agente)
        entorno.agregar_agente(agente)
    
    print(f"\nConfiguración:")
    print(f"  - Grid: {entorno.ancho}x{entorno.alto}")
    print(f"  - Comida inicial: {entorno.get_comida_restante()}")
    print(f"  - Agentes competidores: {len(agentes)}")
    print(f"  - Regeneración: Activada")
    
    input("\nPresiona Enter para comenzar...")
    
    # Simulación
    for paso in range(PASOS_SIMULACION * 2):  # Más pasos para competencia
        # Actualizar agentes
        for agente in agentes:
            if agente.energia > 0:
                agente.update(entorno)
        
        # Avanzar entorno (regenera comida)
        entorno.step()
        
        # Mostrar cada 5 pasos
        if paso % 5 == 0:
            limpiar_pantalla()
            
            mostrar_grid(
                entorno,
                agentes,
                f"EJERCICIO 6 - Paso {paso + 1}",
                {'Comida disponible': entorno.get_comida_restante()}
            )
            
            # Ranking de agentes
            agentes_ordenados = sorted(
                agentes,
                key=lambda a: a.comida_recolectada,
                reverse=True
            )
            
            print("\n🏆 RANKING:")
            for i, agente in enumerate(agentes_ordenados, 1):
                stats = agente.get_estadisticas()
                estado = "💀" if stats['energia'] <= 0 else "✓"
                print(f"  {i}. {agente.id} - {stats['comida_recolectada']} comida "
                      f"- {stats['energia']} energía {estado}")
            
            time.sleep(0.5)
        
        # Verificar si todos están sin energía
        if all(a.energia <= 0 for a in agentes):
            print("\n⚠️  Todos los agentes sin energía")
            break
    
    # Estadísticas finales
    print("\n" + "=" * 70)
    print("RESULTADOS FINALES")
    print("=" * 70)
    
    agentes_ordenados = sorted(
        agentes,
        key=lambda a: a.comida_recolectada,
        reverse=True
    )
    
    print("\n🏆 GANADOR:", agentes_ordenados[0].id)
    print(f"   Comida recolectada: {agentes_ordenados[0].comida_recolectada}")
    
    print("\n📊 Estadísticas detalladas:")
    for agente in agentes_ordenados:
        print(f"\n{agente.id}:")
        stats = agente.get_estadisticas()
        for clave, valor in stats.items():
            print(f"  {clave}: {valor}")


if __name__ == "__main__":
    simular_ejercicio6()
