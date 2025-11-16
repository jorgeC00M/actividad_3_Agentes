# simulaciones/sim_ejercicio4.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
import random

from src.agentes.agente_recolector import AgenteRecolectorComunicativo
from src.entornos.entorno_recoleccion import EntornoRecoleccion
from src.utils.visualizacion import Visualizador
from src.utils.estadisticas import EstadisticasRecoleccion
from src.config.parametros import CONFIG_EJERCICIO_4


def simular_ejercicio4():
    """Ejecuta la simulación del ejercicio 4"""
    print("=== EJERCICIO 4: COMUNICACIÓN ENTRE AGENTES ===")
    print("Objetivo: Implementar comunicación entre agentes para evitar ir al mismo objetivo\n")
    
    config = CONFIG_EJERCICIO_4
    entorno = EntornoRecoleccion(
        config['ancho_grid'], 
        config['alto_grid'], 
        config['num_comida'],
        config['num_obstaculos']
    )
    
    # Crear múltiples agentes comunicativos
    agentes = []
    for i in range(config['num_agentes']):
        x = random.randint(0, config['ancho_grid'] - 1)
        y = random.randint(0, config['alto_grid'] - 1)
        agente = AgenteRecolectorComunicativo(x, y, f"R{i+1}")
        agentes.append(agente)
        entorno.agregar_agente(agente)
    
    estadisticas = EstadisticasRecoleccion()
    visualizador = Visualizador()
    
    print("Leyenda: R1,R2,R3=Agentes, C=Comida, X=Obstáculo")
    print("Estado inicial del entorno:")
    visualizador.mostrar_entorno_recoleccion(entorno, agentes)
    
    # Ejecutar simulación
    for paso in range(config['max_pasos']):
        resultado = entorno.ejecutar_paso()
        estadisticas.registrar_paso(entorno, agentes)
        
        # Permitir que los agentes se comuniquen
        for agente in agentes:
            if hasattr(agente, 'enviar_mensaje'):
                otros_agentes = [a for a in agentes if a.id != agente.id]
                # Compartir comida encontrada
                comida_local = agente.percibir(entorno)
                if comida_local and otros_agentes:
                    for pos in comida_local[:2]:  # Compartir hasta 2 posiciones
                        agente.enviar_mensaje(otros_agentes, 'comida_encontrada', pos)
        
        if paso % 10 == 0 or len(entorno.comida) == 0:
            print(f"--- Paso {paso + 1} ---")
            visualizador.mostrar_entorno_recoleccion(entorno, agentes)
            print(f"Comida restante: {len(entorno.comida)}")
            print(f"Agentes activos: {len(agentes)}")
            
            # Mostrar estadísticas de comunicación
            total_mensajes = sum(len(agente.mensajes) for agente in agentes 
                               if hasattr(agente, 'mensajes'))
            print(f"Mensajes pendientes: {total_mensajes}")
        
        # Condición de terminación
        if len(entorno.comida) == 0:
            print("¡ÉXITO! Toda la comida ha sido recolectada.")
            break
    
    # Resultados finales
    print("\n" + "="*50)
    print("SIMULACIÓN COMPLETADA")
    print("="*50)
    estadisticas.mostrar_resumen(agentes)
    
    # Métricas específicas del ejercicio 4
    print(f"\nMétricas específicas Ejercicio 4:")
    total_mensajes_enviados = 0
    objetivos_reservados = 0
    
    for agente in agentes:
        if hasattr(agente, 'objetivos_reservados'):
            objetivos_reservados += len(agente.objetivos_reservados)
        # Contar mensajes procesados (asumiendo que se limpian después de procesar)
    
    print(f"Objetivos reservados: {objetivos_reservados}")
    print(f"Conflicto evitados: {objetivos_reservados}")
    
    # Eficiencia de colaboración
    comida_por_agente = estadisticas.datos['comida_recolectada'][-1] / len(agentes)
    print(f"Comida promedio por agente: {comida_por_agente:.1f}")


if __name__ == "__main__":
    simular_ejercicio4()