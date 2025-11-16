# simulaciones/sim_ejercicio1.py
from src.agentes.agente_Limpieza import AgenteLimpiezaConMemoria
from src.entornos.entorno_limpieza import EntornoLimpieza
from src.utils.visualizacion import Visualizador
from src.utils.estadisticas import EstadisticasLimpieza
from src.config.parametros import CONFIG_EJERCICIO_1


def simular_ejercicio1():
    """Ejecuta la simulación del ejercicio 1"""
    print("=== EJERCICIO 1: AGENTE LIMPIADOR CON MEMORIA ===")
    print("Objetivo: Implementar un agente que recuerde lugares ya visitados\n")
    
    config = CONFIG_EJERCICIO_1
    entorno = EntornoLimpieza(
        config['ancho_grid'], 
        config['alto_grid'], 
        config['num_suciedad']
    )
    
    agente = AgenteLimpiezaConMemoria(*config['posicion_agente'])
    estadisticas = EstadisticasLimpieza()
    visualizador = Visualizador()
    
    # Configurar simulación
    entorno.agregar_agente(agente)
    estadisticas.iniciar()
    
    print("Estado inicial del entorno:")
    visualizador.mostrar_entorno_limpieza(entorno, agente)
    
    # Ejecutar simulación
    for paso in range(config['max_pasos']):
        resultado = entorno.ejecutar_paso()
        estadisticas.registrar_paso(entorno, agente)
        
        if paso % 5 == 0 or len(entorno.suciedad) == 0:
            print(f"--- Paso {paso + 1} ---")
            visualizador.mostrar_entorno_limpieza(entorno, agente)
            visualizador.mostrar_estadisticas_agente(agente)
        
        # Condición de terminación
        if len(entorno.suciedad) == 0:
            print("¡ÉXITO! Toda la suciedad ha sido limpiada.")
            break
    
    # Resultados finales
    print("\n" + "="*50)
    print("SIMULACIÓN COMPLETADA")
    print("="*50)
    estadisticas.mostrar_resumen(agente)
    
    # Métricas específicas del ejercicio 1
    eficiencia_cobertura = (len(agente.lugares_visitados) / 
                          (config['ancho_grid'] * config['alto_grid']) * 100)
    print(f"\nMétricas específicas Ejercicio 1:")
    print(f"Cobertura del entorno: {eficiencia_cobertura:.1f}%")
    print(f"Lugares visitados únicos: {len(agente.lugares_visitados)}")
    print(f"Pasos ejecutados: {entorno.tiempo}")


if __name__ == "__main__":
    simular_ejercicio1()