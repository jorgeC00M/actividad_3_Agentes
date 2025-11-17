# simulaciones/sim_ejercicio4.py
import random

from src.agentes.agente_recolector import AgenteRecolectorComunicativo
from src.entornos.entorno_recoleccion import EntornoRecoleccion
from src.utils.visualizacion import Visualizador
from src.utils.estadisticas import EstadisticasRecoleccion
from src.config.parametros import CONFIG_EJERCICIO_4


def simular_ejercicio4():
    """Ejecuta la simulación del ejercicio 4."""
    print("=== EJERCICIO 4: COMUNICACIÓN ENTRE AGENTES ===")
    print(
        "Objetivo: Implementar comunicación entre agentes para evitar ir al mismo objetivo.\n"
    )

    base = CONFIG_EJERCICIO_4
    try:
        num_agentes = int(
            input(f"Nº de agentes [{base['num_agentes']}]: ")
            or base["num_agentes"]
        )
        num_comida = int(
            input(f"Nº de recursos de comida [{base['num_comida']}]: ")
            or base["num_comida"]
        )
        num_obst = int(
            input(f"Nº de obstáculos [{base['num_obstaculos']}]: ")
            or base["num_obstaculos"]
        )
    except ValueError:
        print("Valores inválidos, usando configuración por defecto.")
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
        agente = AgenteRecolectorComunicativo(x, y, f"R{i+1}")
        agentes.append(agente)
        entorno.agregar_agente(agente)

    estadisticas = EstadisticasRecoleccion()
    visualizador = Visualizador()

    print("Leyenda: Rx=Agentes, C=Comida, X=Obstáculo")
    print("Estado inicial del entorno:")
    visualizador.mostrar_entorno_recoleccion(entorno, agentes)

    for paso in range(base["max_pasos"]):
        # Comunicación previa al paso: compartir comida encontrada
        for agente in agentes:
            comida_local = agente.percibir(entorno)
            otros_agentes = [a for a in agentes if a.id != agente.id]
            if comida_local and otros_agentes:
                for pos in comida_local[:2]:
                    agente.enviar_mensaje(otros_agentes, "comida_encontrada", pos)
                    agente.enviar_mensaje(otros_agentes, "objetivo_reservado", pos)

        entorno.ejecutar_paso()
        estadisticas.registrar_paso(entorno, agentes)

        if paso % 10 == 0 or len(entorno.comida) == 0:
            print(f"--- Paso {paso + 1} ---")
            visualizador.mostrar_entorno_recoleccion(entorno, agentes)

            print("Estados de agentes:")
            for a in agentes:
                print(
                    f"- {a.id}: pos=({a.x},{a.y}), comida={a.comida_recolectada}, energia={a.energia}"
                )
                print(f"   Objetivos reservados: {list(a.objetivos_reservados)}")
                print(f"   Mensajes enviados: {a.mensajes_enviados}")

            # Eficiencia de coordinación
            comida_total = estadisticas.datos["comida_recolectada"][-1]
            if (paso + 1) * len(agentes) > 0:
                eficiencia = comida_total / ((paso + 1) * len(agentes))
                print(
                    f"Eficiencia de coordinación: {eficiencia:.3f} comida/(paso·agente)"
                )

        if len(entorno.comida) == 0:
            print("¡ÉXITO! Toda la comida ha sido recolectada.")
            break

    print("\n" + "=" * 50)
    print("SIMULACIÓN COMPLETADA")
    print("=" * 50)
    estadisticas.mostrar_resumen(agentes)

    # Métricas específicas
    total_mensajes = sum(a.mensajes_enviados for a in agentes)
    total_objetivos = sum(len(a.objetivos_reservados) for a in agentes)
    print("\nMétricas específicas Ejercicio 4:")
    print(f"Mensajes enviados totales: {total_mensajes}")
    print(f"Objetivos reservados totales (suma): {total_objetivos}")

    try:
        estadisticas.graficar("Ejercicio 4 - Comunicación multiagente")
    except Exception as e:
        print(f"No se pudo graficar: {e}")


if __name__ == "__main__":
    simular_ejercicio4()
