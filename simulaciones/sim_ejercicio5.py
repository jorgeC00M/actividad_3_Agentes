# simulaciones/sim_ejercicio5.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agentes.agente_recolector import AgenteRecolectorConAprendizaje
from src.entornos.entorno_recoleccion import EntornoRecoleccion
from src.utils.visualizacion import Visualizador
from src.utils.estadisticas import EstadisticasRecoleccion
from src.config.parametros import CONFIG_EJERCICIO_5


def simular_ejercicio5():
    """Ejecuta la simulación del ejercicio 5"""
    print("=== EJERCICIO 5: MEMORIA ESPACIAL ===")
    print("Objetivo: Crear un agente que aprenda qué áreas tienen más comida\n")
    
    config = CONFIG_EJERCICIO_5
    entorno = EntornoRecoleccion(
        config['ancho_grid'], 
        config['alto_grid'], 
        config['num_comida'],
        config['num_obstaculos']
    )
    
    agente = AgenteRecolectorConAprendizaje(*config['posicion_agente'], "Aprendiz")
    estadisticas = EstadisticasRecoleccion()
    visualizador = Visualizador()
    
    # Configurar simulación
    entorno.agregar_agente(agente)
    
    print("Estado inicial del entorno:")
    visualizador.mostrar_entorno_recoleccion(entorno, [agente])
    
    # Ejecutar simulación
    for paso in range(config['max_pasos']):
        resultado = entorno.ejecutar_paso()
        estadisticas.registrar_paso(entorno, [agente])
        
        if paso % 12 == 0 or len(entorno.comida) == 0 or agente.energia <= 0:
            print(f"--- Paso {paso + 1} ---")
            visualizador.mostrar_entorno_recoleccion(entorno, [agente])
            visualizador.mostrar_estadisticas_agente(agente)
            print(f"Áreas productivas: {agente.areas_productivas}")
            print(f"Posiciones en memoria: {len(agente.memoria_comida)}")
        
        # Condiciones de terminación
        if len(entorno.comida) == 0:
            print("¡ÉXITO! Toda la comida ha sido recolectada.")
            break
        elif agente.energia <= 0:
            print("¡AGOTADO! El agente se quedó sin energía.")
            break
    
    # Resultados finales
    print("\n" + "="*50)
    print("SIMULACIÓN COMPLETADA")
    print("="*50)
    estadisticas.mostrar_resumen([agente])
    
    # Métricas específicas del ejercicio 5
    print(f"\nMétricas específicas Ejercicio 5:")
    print(f"Áreas productivas identificadas: {len(agente.areas_productivas)}")
    print(f"Posiciones memorizadas: {len(agente.memoria_comida)}")
    
    # Calcular precisión de la memoria
    if agente.memoria_comida:
        posiciones_con_comida = sum(1 for freq in agente.memoria_comida.values() if freq > 0)
        precision = posiciones_con_comida / len(agente.memoria_comida) * 100
        print(f"Precisión de memoria: {precision:.1f}%")
    
    # Eficiencia de aprendizaje
    eficiencia_busqueda = (agente.comida_recolectada / 
                          min(config['num_comida'], entorno.tiempo) * 100)
    print(f"Eficiencia de búsqueda: {eficiencia_busqueda:.1f}%")


if __name__ == "__main__":
    simular_ejercicio5()