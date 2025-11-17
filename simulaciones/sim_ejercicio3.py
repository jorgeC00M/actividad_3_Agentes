# simulaciones/sim_ejercicio3.py
import time

from src.entornos.entorno_limpieza import EntornoLimpiezaConObstaculos
from src.agentes.agente_limpieza import AgenteLimpiezaConEvasion
from src.config.parametros import CONFIG_EJERCICIO_3
from src.utils.visualizacion import Visualizador
from src.utils.estadisticas import EstadisticasLimpieza


def simular_ejercicio3():
    print("=== EJERCICIO 3 (CONSOLa) - EVASIÓN DE OBSTÁCULOS ===")
    print("Objetivo: DETECTAR → EVITAR → REPLANIFICAR el movimiento.\n")

    config = CONFIG_EJERCICIO_3
    entorno = EntornoLimpiezaConObstaculos(
        config["ancho_grid"],
        config["alto_grid"],
        config["num_suciedad"],
        config["num_obstaculos"],
    )
    agente = AgenteLimpiezaConEvasion(*config["posicion_agente"])
    entorno.agregar_agente(agente)

    vis = Visualizador()
    stats = EstadisticasLimpieza()
    stats.iniciar()

    print("Leyenda: A=Agente, X=Obstáculo, *=Suciedad")
    print("Estado inicial del entorno:")
    vis.mostrar_entorno_limpieza(entorno, agente)

    for paso in range(1, config["max_pasos"] + 1):
        entorno.ejecutar_paso()
        stats.registrar_paso(entorno, agente)

        print(f"\n--- Paso {paso} ---")
        vis.mostrar_entorno_limpieza(entorno, agente)

        print("# El agente escanea en un radio de 1 casilla")
        print("Obstáculos detectados en el último escaneo:")
        for info in agente.ultimo_scan:
            simbolo = "🧱" if info["obstaculo"] else "✅ Libre"
            print(f"- {info['direccion'].capitalize()}: {info['pos']} → {simbolo}")

        print(
            f"Pos: ({agente.x},{agente.y}) | Energía: {agente.energia} | "
            f"Suciedad limpiada: {agente.suciedad_limpiada} | "
            f"Obstáculos detectados: {len(agente.obstaculos_detectados)}"
        )

        if len(entorno.suciedad) == 0:
            print("\n¡ÉXITO! Toda la suciedad ha sido limpiada.")
            break
        if agente.energia <= 0:
            print("\n¡AGOTADO! El agente se quedó sin energía.")
            break

        time.sleep(0.1)

    print("\n=== RESULTADOS FINALES EJERCICIO 3 ===")
    stats.mostrar_resumen(agente)
    print(f"Obstáculos totales: {config['num_obstaculos']}")
    print(f"Obstáculos detectados: {len(agente.obstaculos_detectados)}")
    print(f"Pasos ejecutados: {entorno.tiempo}")


if __name__ == "__main__":
    simular_ejercicio3()
