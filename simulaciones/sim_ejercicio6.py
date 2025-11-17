# simulaciones/sim_ejercicio6.py
import time
import random

from src.entornos.entorno_recoleccion import EntornoRecoleccionCompetitivo
from src.agentes.agente_recolector import AgenteCompetitivo
from src.config.parametros import CONFIG_EJERCICIO_6
from src.utils.visualizacion import Visualizador
from src.utils.estadisticas import EstadisticasRecoleccion


def simular_ejercicio6():
    print("=== EJERCICIO 6 (CONSOLa) - COMPETENCIA POR RECURSOS ===")
    print("Objetivo: Agentes con estrategias distintas compiten por comida limitada.\n")

    base = CONFIG_EJERCICIO_6
    print("Config (vacío = por defecto):")
    try:
        num_agentes = int(
            input(f"Nº de agentes [{base['num_agentes']}]: ")
            or base["num_agentes"]
        )
        num_comida = int(
            input(f"Nº de comida [{base['num_comida']}]: ")
            or base["num_comida"]
        )
    except ValueError:
        num_agentes = base["num_agentes"]
        num_comida = base["num_comida"]

    entorno = EntornoRecoleccionCompetitivo(
        base["ancho_grid"], base["alto_grid"], num_comida, base["num_obstaculos"]
    )

    agentes = []
    estrategias = base["estrategias"]
    for i in range(num_agentes):
        x = random.randint(0, base["ancho_grid"] - 1)
        y = random.randint(0, base["alto_grid"] - 1)
        estrategia = estrategias[i] if i < len(estrategias) else "agresiva"
        a = AgenteCompetitivo(x, y, f"{estrategia[0].upper()}{i+1}", estrategia)
        agentes.append(a)
        entorno.agregar_agente(a)

    vis = Visualizador()
    stats = EstadisticasRecoleccion()

    print("Leyenda: A=Agresivo, C=Conservador, E=Evasivo, C=comida, X=obstáculo")
    print("Estado inicial del entorno:")
    vis.mostrar_entorno_recoleccion(entorno, agentes)

    for paso in range(1, base["max_pasos"] + 1):
        entorno.ejecutar_paso()
        stats.registrar_paso(entorno, agentes)

        print(f"\n--- Paso {paso} ---")
        vis.mostrar_entorno_recoleccion(entorno, agentes)
        print(f"Comida restante: {len(entorno.comida)}")

        for a in agentes:
            conflictos = a.conflictos_ganados + a.conflictos_perdidos
            print(
                f"{a.id} ({a.estrategia}): pos=({a.x},{a.y}), "
                f"comida={a.comida_recolectada}, energia={a.energia}, "
                f"conflictos={conflictos} (G={a.conflictos_ganados}, P={a.conflictos_perdidos})"
            )

        if len(entorno.comida) == 0 and paso > 5:
            print("\n¡RECURSOS AGOTADOS! No queda comida en el entorno.")
            break

        time.sleep(0.1)

    print("\n=== RESULTADOS FINALES EJERCICIO 6 ===")
    stats.mostrar_resumen(agentes)

    if agentes:
        ganador = max(agentes, key=lambda a: a.comida_recolectada)
        print(
            f"\n🏆 GANADOR: {ganador.id} con {ganador.comida_recolectada} comida "
            f"(estrategia: {ganador.estrategia})"
        )

    estrategias_dict = {}
    for a in agentes:
        estrategias_dict.setdefault(a.estrategia, []).append(a)

    print("\nAnálisis por estrategia:")
    for estrategia, grupo in estrategias_dict.items():
        comida_total = sum(a.comida_recolectada for a in grupo)
        conflictos_total = sum(
            a.conflictos_ganados + a.conflictos_perdidos for a in grupo
        )
        print(f"\nEstrategia {estrategia.upper()}:")
        print(f"  Agentes: {len(grupo)}")
        print(f"  Comida total: {comida_total}")
        print(f"  Conflictos totales: {conflictos_total}")
        if conflictos_total > 0:
            ratio = (
                sum(a.conflictos_ganados for a in grupo)
                / conflictos_total
                * 100
            )
            print(f"  Ratio de conflictos ganados: {ratio:.1f}%")

    print(f"\nPasos ejecutados: {entorno.tiempo}")


if __name__ == "__main__":
    simular_ejercicio6()
