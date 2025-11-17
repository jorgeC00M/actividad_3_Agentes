# simulaciones/sim_ejercicio6.py
import random

from src.agentes.agente_recolector import AgenteCompetitivo
from src.entornos.entorno_recoleccion import EntornoRecoleccionCompetitivo
from src.utils.visualizacion import Visualizador
from src.utils.estadisticas import EstadisticasRecoleccion
from src.config.parametros import CONFIG_EJERCICIO_6


def simular_ejercicio6():
    """Ejecuta la simulación del ejercicio 6."""
    print("=== EJERCICIO 6: COMPETENCIA POR RECURSOS ===")
    print("Objetivo: Sistema donde agentes compiten por recursos limitados.\n")

    base = CONFIG_EJERCICIO_6
    try:
        num_agentes = int(
            input(f"Nº de agentes en competencia [{base['num_agentes']}]: ")
            or base["num_agentes"]
        )
        num_comida = int(
            input(f"Nº de recursos de comida [{base['num_comida']}]: ")
            or base["num_comida"]
        )
    except ValueError:
        num_agentes = base["num_agentes"]
        num_comida = base["num_comida"]

    entorno = EntornoRecoleccionCompetitivo(
        base["ancho_grid"],
        base["alto_grid"],
        num_comida,
        base["num_obstaculos"],
    )

    agentes = []
    estrategias = base["estrategias"]
    for i in range(num_agentes):
        x = random.randint(0, base["ancho_grid"] - 1)
        y = random.randint(0, base["alto_grid"] - 1)
        estrategia = (
            estrategias[i] if i < len(estrategias) else "agresiva"
        )
        agente = AgenteCompetitivo(x, y, f"{estrategia[0].upper()}{i+1}", estrategia)
        agentes.append(agente)
        entorno.agregar_agente(agente)

    estadisticas = EstadisticasRecoleccion()
    visualizador = Visualizador()

    print(
        "Leyenda: A1,G2=Agentes (A=Agresivo, C=Conservador, E=Evasivo), C=Comida, X=Obstáculo"
    )
    print("Estado inicial del entorno:")
    visualizador.mostrar_entorno_recoleccion(entorno, agentes)

    for paso in range(base["max_pasos"]):
        entro_result = entorno.ejecutar_paso()
        estadisticas.registrar_paso(entorno, agentes)

        if (
            paso % 10 == 0
            or len(entorno.comida) == 0
            or len(agentes) == 0
        ):
            print(f"--- Paso {paso + 1} ---")
            visualizador.mostrar_entorno_recoleccion(entorno, agentes)
            print(f"Comida restante: {len(entorno.comida)}")
            print(f"Agentes activos: {len(agentes)}")

            for a in agentes:
                conflictos = (
                    a.conflictos_ganados + a.conflictos_perdidos
                )
                print(
                    f"{a.id} ({a.estrategia}): comida={a.comida_recolectada}, conflictos={conflictos}"
                )

        if len(entorno.comida) == 0 and paso > 5:
            print("¡RECURSOS AGOTADOS! No queda comida en el entorno.")
            break
        if len(agentes) == 0:
            print("¡TODOS ELIMINADOS! Ningún agente sobrevivió.")
            break

    print("\n" + "=" * 50)
    print("COMPETENCIA FINALIZADA")
    print("=" * 50)
    estadisticas.mostrar_resumen(agentes)

    print("\nMétricas específicas Ejercicio 6:")
    estrategias_dict = {}
    for a in agentes:
        estrategias_dict.setdefault(a.estrategia, []).append(a)

    for estrategia, group in estrategias_dict.items():
        comida_total = sum(a.comida_recolectada for a in group)
        conflictos_total = sum(
            a.conflictos_ganados + a.conflictos_perdidos for a in group
        )
        print(f"\nEstrategia {estrategia.upper()}:")
        print(f"  Agentes: {len(group)}")
        print(f"  Comida total: {comida_total}")
        print(f"  Conflictos totales: {conflictos_total}")
        if conflictos_total > 0:
            ratio_ganados = (
                sum(a.conflictos_ganados for a in group)
                / conflictos_total
                * 100
            )
            print(f"  Ratio de conflictos ganados: {ratio_ganados:.1f}%")

    if agentes:
        ganador = max(agentes, key=lambda a: a.comida_recolectada)
        print(
            f"\n🏆 GANADOR: {ganador.id} con {ganador.comida_recolectada} unidades de comida"
        )

    try:
        estadisticas.graficar("Ejercicio 6 - Competencia por recursos")
    except Exception as e:
        print(f"No se pudo graficar: {e}")


if __name__ == "__main__":
    simular_ejercicio6()
