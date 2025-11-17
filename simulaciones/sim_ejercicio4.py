# simulaciones/sim_ejercicio4.py
import time
import random

from src.entornos.entorno_recoleccion import EntornoRecoleccion
from src.agentes.agente_recolector import AgenteRecolectorComunicativo
from src.config.parametros import CONFIG_EJERCICIO_4
from src.utils.visualizacion import Visualizador
from src.utils.estadisticas import EstadisticasRecoleccion


def simular_ejercicio4():
    print("=== EJERCICIO 4 (CONSOLa) - COMUNICACIÓN ENTRE RECOLECTORES ===")
    print("Objetivo: Coordinarse para NO ir al mismo objetivo.\n")

    base = CONFIG_EJERCICIO_4
    print("Config (vacío = por defecto):")
    try:
        num_agentes = int(
            input(f"Nº de agentes [{base['num_agentes']}]: ") or base["num_agentes"]
        )
        num_comida = int(
            input(f"Nº de comida [{base['num_comida']}]: ") or base["num_comida"]
        )
        num_obst = int(
            input(f"Nº de obstáculos [{base['num_obstaculos']}]: ")
            or base["num_obstaculos"]
        )
    except ValueError:
        num_agentes = base["num_agentes"]
        num_comida = base["num_comida"]
        num_obst = base["num_obstaculos"]

    entorno = EntornoRecoleccion(
        base["ancho_grid"], base["alto_grid"], num_comida, num_obst
    )

    agentes = []
    for i in range(num_agentes):
        x = random.randint(0, base["ancho_grid"] - 1)
        y = random.randint(0, base["alto_grid"] - 1)
        a = AgenteRecolectorComunicativo(x, y, f"R{i+1}")
        agentes.append(a)
        entorno.agregar_agente(a)

    vis = Visualizador()
    stats = EstadisticasRecoleccion()

    print("Leyenda: Ri=agentes, C=comida, X=obstáculo")
    print("Estado inicial del entorno:")
    vis.mostrar_entorno_recoleccion(entorno, agentes)

    for paso in range(1, base["max_pasos"] + 1):
        # Comunicación
        for agente in agentes:
            comida_local = agente.percibir(entorno)
            otros = [a for a in agentes if a.id != agente.id]
            if comida_local and otros:
                for pos in comida_local[:2]:
                    agente.enviar_mensaje(otros, "comida_encontrada", pos)
                    agente.enviar_mensaje(otros, "objetivo_reservado", pos)

        entorno.ejecutar_paso()
        stats.registrar_paso(entorno, agentes)

        print(f"\n--- Paso {paso} ---")
        vis.mostrar_entorno_recoleccion(entorno, agentes)
        print(f"Comida restante: {len(entorno.comida)}")

        for a in agentes:
            print(
                f"{a.id}: pos=({a.x},{a.y}), comida={a.comida_recolectada}, "
                f"energia={a.energia}, objetivos_reservados={list(a.objetivos_reservados)}"
            )

        if len(entorno.comida) == 0:
            print("\n¡ÉXITO! Toda la comida ha sido recolectada.")
            break

        time.sleep(0.1)

    print("\n=== RESULTADOS FINALES EJERCICIO 4 ===")
    stats.mostrar_resumen(agentes)

    comida_total = sum(a.comida_recolectada for a in agentes)
    total_mensajes = sum(getattr(a, "mensajes_enviados", 0) for a in agentes)
    objetivos_res = sum(len(a.objetivos_reservados) for a in agentes)

    print(f"Comida total recolectada: {comida_total}")
    print(f"Mensajes enviados totales: {total_mensajes}")
    print(f"Objetivos reservados totales: {objetivos_res}")
    if paso > 0 and len(agentes) > 0:
        eficiencia = comida_total / (paso * len(agentes))
        print(f"Eficiencia de coordinación: {eficiencia:.3f} comida/(paso·agente)")


if __name__ == "__main__":
    simular_ejercicio4()
