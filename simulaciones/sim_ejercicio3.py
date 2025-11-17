# simulaciones/sim_ejercicio3.py
from src.agentes.agente_limpieza import AgenteLimpiezaConEvasion
from src.entornos.entorno_limpieza import EntornoLimpiezaConObstaculos
from src.utils.visualizacion import Visualizador
from src.utils.estadisticas import EstadisticasLimpieza
from src.config.parametros import CONFIG_EJERCICIO_3


def simular_ejercicio3():
    """Ejecuta la simulación del ejercicio 3."""
    print("=== EJERCICIO 3: EVASIÓN DE OBSTÁCULOS ===")
    print("Objetivo: Implementar un agente que evite obstáculos fijos en el entorno.\n")

    config = CONFIG_EJERCICIO_3
    entorno = EntornoLimpiezaConObstaculos(
        config["ancho_grid"],
        config["alto_grid"],
        config["num_suciedad"],
        config["num_obstaculos"],
    )

    agente = AgenteLimpiezaConEvasion(*config["posicion_agente"])
    estadisticas = EstadisticasLimpieza()
    visualizador = Visualizador()

    entorno.agregar_agente(agente)
    estadisticas.iniciar()

    print("Leyenda: A=Agente, X=Obstáculo, *=Suciedad")
    print("Estado inicial del entorno:")
    visualizador.mostrar_entorno_limpieza(entorno, agente)

    for paso in range(config["max_pasos"]):
        entorno.ejecutar_paso()
        estadisticas.registrar_paso(entorno, agente)

        if (
            paso % 5 == 0
            or len(entorno.suciedad) == 0
            or agente.energia <= 0
        ):
            print(f"--- Paso {paso + 1} ---")
            visualizador.mostrar_entorno_limpieza(entorno, agente)
            visualizador.mostrar_estadisticas_agente(agente)

            print("# El agente escanea en un radio de 1 casilla")
            print("Obstáculos detectados en el último escaneo:")
            for info in agente.ultimo_scan:
                simbolo = "🧱" if info["obstaculo"] else "✅ Libre"
                print(
                    f"- {info['direccion'].capitalize()}: {info['pos']} → {simbolo}"
                )

        if len(entorno.suciedad) == 0:
            print("¡ÉXITO! Toda la suciedad ha sido limpiada.")
            break
        if agente.energia <= 0:
            print("¡AGOTADO! El agente se quedó sin energía.")
            break

    print("\n" + "=" * 50)
    print("SIMULACIÓN COMPLETADA")
    print("=" * 50)
    estadisticas.mostrar_resumen(agente)

    celdas_accesibles = (
        config["ancho_grid"] * config["alto_grid"] - config["num_obstaculos"]
    )
    eficiencia_navegacion = (
        len(getattr(agente, "historial_movimientos", [])) / celdas_accesibles * 100
    )

    print("\nMétricas específicas Ejercicio 3:")
    print(f"Obstáculos en el entorno: {config['num_obstaculos']}")
    print(f"Obstáculos detectados: {len(agente.obstaculos_detectados)}")
    print(f"Eficiencia de navegación (aprox): {eficiencia_navegacion:.1f}%")

    print("\nCamino recorrido (x, y, acción):")
    for paso in agente.historial_movimientos:
        print(f"({paso['x']},{paso['y']}) -> {paso['accion']}")

    try:
        estadisticas.graficar("Ejercicio 3 - Evasión de obstáculos")
    except Exception as e:
        print(f"No se pudo graficar: {e}")


if __name__ == "__main__":
    simular_ejercicio3()
