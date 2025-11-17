# simulaciones/sim_ejercicio5.py
import time
import random

from src.entornos.entorno_recoleccion import EntornoRecoleccion
from src.agentes.agente_recolector import AgenteRecolectorConAprendizaje
from src.config.parametros import CONFIG_EJERCICIO_5
from src.utils.visualizacion import Visualizador
from src.utils.estadisticas import EstadisticasRecoleccion


def distribuir_comida_por_areas(entorno, base_num: int):
    """Área 3 > Área 1 > Área 2 > Área 4."""
    ancho, alto = entorno.ancho, entorno.alto
    entorno.comida.clear()

    a1 = int(base_num * 0.3)
    a2 = int(base_num * 0.2)
    a3 = int(base_num * 0.4)
    a4 = max(base_num - (a1 + a2 + a3), 0)

    def generar_en_rect(x0, y0, x1, y1, n):
        for _ in range(n):
            x = random.randint(x0, x1)
            y = random.randint(y0, y1)
            if (x, y) not in entorno.obstaculos:
                entorno.comida[(x, y)] = 1

    mid_x = ancho // 2
    mid_y = alto // 2

    generar_en_rect(0, 0, mid_x - 1, mid_y - 1, a1)          # A1
    generar_en_rect(mid_x, 0, ancho - 1, mid_y - 1, a2)      # A2
    generar_en_rect(0, mid_y, mid_x - 1, alto - 1, a3)       # A3
    generar_en_rect(mid_x, mid_y, ancho - 1, alto - 1, a4)   # A4


def simular_ejercicio5():
    print("=== EJERCICIO 5 (CONSOLa) - MEMORIA ESPACIAL ===")
    print("Objetivo: El agente aprende qué ÁREAS tienen más comida.\n")
    print("Áreas: 4 zonas, con prioridad: Área 3 > Área 1 > Área 2 > Área 4.\n")

    config = CONFIG_EJERCICIO_5
    entorno = EntornoRecoleccion(
        config["ancho_grid"],
        config["alto_grid"],
        config["num_comida"],
        config["num_obstaculos"],
    )

    distribuir_comida_por_areas(entorno, config["num_comida"])

    agente = AgenteRecolectorConAprendizaje(*config["posicion_agente"], "Aprendiz")
    entorno.agregar_agente(agente)

    vis = Visualizador()
    stats = EstadisticasRecoleccion()

    print("Estado inicial del entorno:")
    vis.mostrar_entorno_recoleccion(entorno, [agente])

    for paso in range(1, config["max_pasos"] + 1):
        entorno.ejecutar_paso()
        stats.registrar_paso(entorno, [agente])

        print(f"\n--- Paso {paso} ---")
        vis.mostrar_entorno_recoleccion(entorno, [agente])
        print(
            f"Pos=({agente.x},{agente.y}), comida={agente.comida_recolectada}, "
            f"energia={agente.energia}"
        )
        print(f"Áreas productivas: {agente.areas_productivas}")
        print(f"Posiciones en memoria: {len(agente.memoria_comida)}")

        if len(entorno.comida) == 0:
            print("\n¡ÉXITO! Toda la comida ha sido recolectada.")
            break
        if agente.energia <= 0:
            print("\n¡AGOTADO! El agente se quedó sin energía.")
            break

        time.sleep(0.1)

    print("\n=== RESULTADOS FINALES EJERCICIO 5 ===")
    stats.mostrar_resumen([agente])
    print(f"Áreas productivas identificadas: {len(agente.areas_productivas)}")
    print(f"Posiciones memorizadas: {len(agente.memoria_comida)}")

    if agente.memoria_comida:
        posiciones_con_comida = sum(
            1 for freq in agente.memoria_comida.values() if freq > 0
        )
        precision = posiciones_con_comida / len(agente.memoria_comida) * 100
        print(f"Precisión de memoria: {precision:.1f}%")

    if paso > 0:
        eficiencia_busqueda = agente.comida_recolectada / paso * 100
        print(f"Eficiencia de búsqueda: {eficiencia_busqueda:.1f}%")

    try:
        agente.guardar_memoria_areas()
        print("Memoria de áreas productivas guardada (para próxima ejecución).")
    except Exception:
        pass


if __name__ == "__main__":
    simular_ejercicio5()
