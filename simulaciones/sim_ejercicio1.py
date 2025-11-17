# simulaciones/sim_ejercicio1.py
import time

from src.entornos.entorno_limpieza import EntornoLimpieza
from src.agentes.agente_limpieza import AgenteLimpiezaConMemoria
from src.config.parametros import CONFIG_EJERCICIO_1
from src.utils.visualizacion import Visualizador
from src.utils.estadisticas import EstadisticasLimpieza


def simular_ejercicio1():
    print("=== EJERCICIO 1 (CONSOLa) - AGENTE LIMPIADOR CON MEMORIA ===")
    print("Objetivo: El agente recuerda lugares visitados y evita repetir celdas.\n")

    config = CONFIG_EJERCICIO_1
    entorno = EntornoLimpieza(
        config["ancho_grid"], config["alto_grid"], config["num_suciedad"]
    )
    agente = AgenteLimpiezaConMemoria(*config["posicion_agente"])
    entorno.agregar_agente(agente)

    vis = Visualizador()
    stats = EstadisticasLimpieza()
    stats.iniciar()

    print("Estado inicial del entorno:")
    vis.mostrar_entorno_limpieza(entorno, agente)

    for paso in range(1, config["max_pasos"] + 1):
        entorno.ejecutar_paso()
        stats.registrar_paso(entorno, agente)

        print(f"\n--- Paso {paso} ---")
        vis.mostrar_entorno_limpieza(entorno, agente)
        print(
            f"Posición: ({agente.x},{agente.y}) | Energía: {agente.energia} | "
            f"Suciedad limpiada: {agente.suciedad_limpiada} | Lugares visitados: {len(agente.lugares_visitados)}"
        )

        if len(entorno.suciedad) == 0:
            print("\n¡ÉXITO! Toda la suciedad ha sido limpiada.")
            break

        time.sleep(0.1)

    print("\n=== RESULTADOS FINALES EJERCICIO 1 ===")
    stats.mostrar_resumen(agente)

    total_celdas = entorno.ancho * entorno.alto
    cobertura = (
        len(agente.lugares_visitados) / total_celdas * 100 if total_celdas > 0 else 0
    )
    print(f"Cobertura del entorno: {cobertura:.1f}%")
    print(f"Pasos ejecutados: {entorno.tiempo}")


if __name__ == "__main__":
    simular_ejercicio1()
