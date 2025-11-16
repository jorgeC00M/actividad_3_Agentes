"""
Simulación Ejercicio 3: Agente que evita obstáculos fijos
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agentes.agente_Limpieza import AgenteLimpiezaConEvasion
from src.entornos.entorno_limpieza import EntornoLimpiezaConObstaculos
from src.utils.visualizacion import Visualizador
from src.utils.estadisticas import EstadisticasLimpieza
from src.config.parametros import CONFIG_EJERCICIO_3


def simular_ejercicio3():
    """Ejecuta la simulación del ejercicio 3"""
    print("=== EJERCICIO 3: EVASIÓN DE OBSTÁCULOS ===")
    print("Objetivo: Implementar un agente que evite obstáculos fijos en el entorno\n")
    
    config = CONFIG_EJERCICIO_3
    entorno = EntornoLimpiezaConObstaculos(
        config['ancho_grid'], 
        config['alto_grid'], 
        config['num_suciedad'],
        config['num_obstaculos']
    )
    
    agente = AgenteLimpiezaConEvasion(*config['posicion_agente'])
    estadisticas = EstadisticasLimpieza()
    visualizador = Visualizador()
    
    # Configurar simulación
    entorno.agregar_agente(agente)
    estadisticas.iniciar()
    
    print("Leyenda: A=Agente, X=Obstáculo, *=Suciedad")
    print("Estado inicial del entorno:")
    visualizador.mostrar_entorno_limpieza(entorno, agente)
    
    # Ejecutar simulación
    for paso in range(config['max_pasos']):
        resultado = entorno.ejecutar_paso()
        estadisticas.registrar_paso(entorno, agente)
        
        if paso % 8 == 0 or len(entorno.suciedad) == 0 or agente.energia <= 0:
            print(f"--- Paso {paso + 1} ---")
            visualizador.mostrar_entorno_limpieza(entorno, agente)
            visualizador.mostrar_estadisticas_agente(agente)
            print(f"Obstáculos detectados: {len(agente.obstaculos_detectados)}")
        
        # Condiciones de terminación
        if len(entorno.suciedad) == 0:
            print("¡ÉXITO! Toda la suciedad ha sido limpiada.")
            break
        elif agente.energia <= 0:
            print("¡AGOTADO! El agente se quedó sin energía.")
            break
    
    # Resultados finales
    print("\n" + "="*50)
    print("SIMULACIÓN COMPLETADA")
    print("="*50)
    estadisticas.mostrar_resumen(agente)
    
    # Métricas específicas del ejercicio 3
    celdas_accesibles = (config['ancho_grid'] * config['alto_grid'] - 
                        config['num_obstaculos'])
    eficiencia_navegacion = (len(agente.lugares_visitados) / celdas_accesibles * 100)
    
    print(f"\nMétricas específicas Ejercicio 3:")
    print(f"Obstáculos en el entorno: {config['num_obstaculos']}")
    print(f"Obstáculos detectados: {len(agente.obstaculos_detectados)}")
    print(f"Eficiencia de navegación: {eficiencia_navegacion:.1f}%")
    print(f"Colisiones evitadas: {len(agente.obstaculos_detectados)}")


if __name__ == "__main__":
    simular_ejercicio3()