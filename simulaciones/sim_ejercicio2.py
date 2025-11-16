"""
Simulación Ejercicio 2: Diferentes tipos de suciedad con distintos valores
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agentes.agente_Limpieza import AgenteLimpiezaConTipos
from src.entornos.entorno_limpieza import EntornoLimpiezaConTipos
from src.utils.visualizacion import Visualizador
from src.utils.estadisticas import EstadisticasLimpieza
from src.config.parametros import CONFIG_EJERCICIO_2


def simular_ejercicio2():
    """Ejecuta la simulación del ejercicio 2"""
    print("=== EJERCICIO 2: TIPOS DE SUCIEDAD CON VALORES ===")
    print("Objetivo: Agregar diferentes tipos de suciedad con distintos valores\n")
    
    config = CONFIG_EJERCICIO_2
    entorno = EntornoLimpiezaConTipos(
        config['ancho_grid'], 
        config['alto_grid'], 
        config['num_suciedad']
    )
    
    agente = AgenteLimpiezaConTipos(*config['posicion_agente'])
    estadisticas = EstadisticasLimpieza()
    visualizador = Visualizador()
    
    # Configurar simulación
    entorno.agregar_agente(agente)
    estadisticas.iniciar()
    
    print("Leyenda: P=Polvo(1p), M=Mancha(2p), B=Barro(3p)")
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
    
    # Métricas específicas del ejercicio 2
    print(f"\nMétricas específicas Ejercicio 2:")
    print(f"Puntos por tipo de suciedad:")
    for tipo, cantidad in agente.tipos_limpiados.items():
        valor = entorno.tipos_suciedad[tipo]['valor']
        puntos_tipo = cantidad * valor
        print(f"  {tipo}: {cantidad} unidades × {valor}p = {puntos_tipo}p")
    
    eficiencia_puntos = (agente.puntos_totales / 
                        (sum(env['valor'] for env in entorno.tipos_suciedad.values()) * 
                         config['num_suciedad']) * 100)
    print(f"\nEficiencia en puntos: {eficiencia_puntos:.1f}%")


if __name__ == "__main__":
    simular_ejercicio2()