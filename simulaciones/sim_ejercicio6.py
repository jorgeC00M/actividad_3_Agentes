# simulaciones/sim_ejercicio6.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
import random

from src.agentes.agente_recolector import AgenteCompetitivo
from src.entornos.entorno_recoleccion import EntornoRecoleccionCompetitivo
from src.utils.visualizacion import Visualizador
from src.utils.estadisticas import EstadisticasRecoleccion
from src.config.parametros import CONFIG_EJERCICIO_6


def simular_ejercicio6():
    """Ejecuta la simulación del ejercicio 6"""
    print("=== EJERCICIO 6: COMPETENCIA POR RECURSOS ===")
    print("Objetivo: Desarrollar un sistema donde agentes compitan por recursos limitados\n")
    
    config = CONFIG_EJERCICIO_6
    entorno = EntornoRecoleccionCompetitivo(
        config['ancho_grid'], 
        config['alto_grid'], 
        config['num_comida'],
        config['num_obstaculos']
    )
    
    # Crear agentes con diferentes estrategias
    agentes = []
    for i in range(config['num_agentes']):
        x = random.randint(0, config['ancho_grid'] - 1)
        y = random.randint(0, config['alto_grid'] - 1)
        estrategia = config['estrategias'][i] if i < len(config['estrategias']) else 'agresiva'
        agente = AgenteCompetitivo(x, y, f"{estrategia[0].upper()}{i+1}", estrategia)
        agentes.append(agente)
        entorno.agregar_agente(agente)
    
    estadisticas = EstadisticasRecoleccion()
    visualizador = Visualizador()
    
    print("Leyenda: A1,G2=Agentes (A=Agresivo, C=Conservador, E=Evasivo), C=Comida, X=Obstáculo")
    print("Estado inicial del entorno:")
    visualizador.mostrar_entorno_recoleccion(entorno, agentes)
    
    # Ejecutar simulación
    for paso in range(config['max_pasos']):
        resultado = entorno.ejecutar_paso()
        estadisticas.registrar_paso(entorno, agentes)
        
        # Comunicación entre agentes competitivos
        for agente in agentes:
            if hasattr(agente, 'enviar_mensaje'):
                otros_agentes = [a for a in agentes if a.id != agente.id]
                comida_local = agente.percibir(entorno)
                if comida_local and otros_agentes:
                    for pos in comida_local[:1]:  # Compartir menos información
                        agente.enviar_mensaje(otros_agentes, 'comida_encontrada', pos)
                        agente.enviar_mensaje(otros_agentes, 'objetivo_reservado', pos)
        
        if paso % 15 == 0 or len(entorno.comida) == 0 or len(agentes) == 0:
            print(f"--- Paso {paso + 1} ---")
            visualizador.mostrar_entorno_recoleccion(entorno, agentes)
            print(f"Comida restante: {len(entorno.comida)}")
            print(f"Agentes activos: {len(agentes)}")
            
            # Mostrar estado de competencia
            for agente in agentes:
                conflictos = (getattr(agente, 'conflictos_ganados', 0) + 
                            getattr(agente, 'conflictos_perdidos', 0))
                print(f"{agente.id}: {agente.comida_recolectada} comida, {conflictos} conflictos")
        
        # Condiciones de terminación
        if len(entorno.comida) == 0 and paso > 10:
            print("¡RECURSOS AGOTADOS! No queda comida en el entorno.")
            break
        elif len(agentes) == 0:
            print("¡TODOS ELIMINADOS! Ningún agente sobrevivió.")
            break
    
    # Resultados finales
    print("\n" + "="*50)
    print("COMPETENCIA FINALIZADA")
    print("="*50)
    estadisticas.mostrar_resumen(agentes)
    
    # Métricas específicas del ejercicio 6
    print(f"\nMétricas específicas Ejercicio 6:")
    
    # Análisis por estrategia
    estrategias = {}
    for agente in agentes:
        if hasattr(agente, 'estrategia'):
            estrategia = agente.estrategia
            if estrategia not in estrategias:
                estrategias[estrategia] = []
            estrategias[estrategia].append(agente)
    
    for estrategia, agents in estrategias.items():
        comida_total = sum(a.comida_recolectada for a in agents)
        conflictos_total = sum(getattr(a, 'conflictos_ganados', 0) + 
                             getattr(a, 'conflictos_perdidos', 0) for a in agents)
        print(f"\nEstrategia {estrategia.upper()}:")
        print(f"  Agentes: {len(agents)}")
        print(f"  Comida total: {comida_total}")
        print(f"  Conflictos totales: {conflictos_total}")
        if conflictos_total > 0:
            ratio_ganados = sum(getattr(a, 'conflictos_ganados', 0) for a in agents) / conflictos_total * 100
            print(f"  Ratio de conflictos ganados: {ratio_ganados:.1f}%")
    
    # Ganador de la competencia
    if agentes:
        ganador = max(agentes, key=lambda a: a.comida_recolectada)
        print(f"\n🏆 GANADOR: {ganador.id} con {ganador.comida_recolectada} comida")
        if hasattr(ganador, 'estrategia'):
            print(f"   Estrategia: {ganador.estrategia}")


if __name__ == "__main__":
    simular_ejercicio6()