# simulaciones/sim_ejercicio5.py
from src.agentes.agente_recolector import AgenteRecolectorConAprendizaje
from src.entornos.entorno_recoleccion import EntornoRecoleccion
from src.utils.visualizacion import Visualizador
from src.utils.estadisticas import EstadisticasRecoleccion
from src.config.parametros import CONFIG_EJERCICIO_5


def distribuir_comida_por_areas(entorno, base_num):
    """
    Divide el grid en 4 áreas y distribuye comida:
    Área 3 > Área 1 > Área 2 > Área 4.
    """
    ancho, alto = entorno.ancho, entorno.alto
    entorno.comida.clear()

    # Cuadrantes:
    # A1: arriba-izquierda
    # A2: arriba-derecha
    # A3: abajo-izquierda
    # A4: abajo-derecha
    a1 = int(base_num * 0.3)
    a2 = int(base_num * 0.2)
    a3 = int(base_num * 0.4)  # más comida
    a4 = max(base_num - (a1 + a2 + a3), 0)

    def generar_en_rect(x0, y0, x1, y1, n):
        import random

        for _ in range(n):
            x = random.randint(x0, x1)
            y = random.randint(y0, y1)
            if (x, y) not in entorno.obstaculos:
                entorno.comida[(x, y)] = 1

    mid_x = ancho // 2
    mid_y = alto // 2

    generar_en_rect(0, 0, mid_x - 1, mid_y - 1, a1)  # A1
    generar_en_rect(mid_x, 0, ancho - 1, mid_y - 1, a2)  # A2
    generar_en_rect(0, mid_y, mid_x - 1, alto - 1, a3)  # A3
    generar_en_rect(mid_x, mid_y, ancho - 1, alto - 1, a4)  # A4


def simular_ejercicio5():
    """Ejecuta la simulación del ejercicio 5."""
    print("=== EJERCICIO 5: MEMORIA ESPACIAL ===")
    print(
        "Objetivo: Crear un agente que aprenda qué áreas tienen más comida (Aprendizaje rápido).\n"
    )

    config = CONFIG_EJERCICIO_5
    try:
        pasos_max = int(
            input(f"Nº máximo de pasos [{config['max_pasos']}]: ")
            or config["max_pasos"]
        )
    except ValueError:
        pasos_max = config["max_pasos"]

    entorno = EntornoRecoleccion(
        config["ancho_grid"],
        config["alto_grid"],
        config["num_comida"],
        config["num_obstaculos"],
    )

    # Reorganizar comida por áreas
    distribuir_comida_por_areas(entorno, config["num_comida"])

    agente = AgenteRecolectorConAprendizaje(
        *config["posicion_agente"], "Aprendiz"
    )
    estadisticas = EstadisticasRecoleccion()
    visualizador = Visualizador()

    entorno.agregar_agente(agente)

    print("Estado inicial del entorno (área 3 con más comida):")
    visualizador.mostrar_entorno_recoleccion(entorno, [agente])

    for paso in range(pasos_max):
        entorno.ejecutar_paso()
        estadisticas.registrar_paso(entorno, [agente])

        if (
            paso % 10 == 0
            or len(entorno.comida) == 0
            or agente.energia <= 0
        ):
            print(f"--- Paso {paso + 1} ---")
            visualizador.mostrar_entorno_recoleccion(entorno, [agente])
            visualizador.mostrar_estadisticas_agente(agente)
            print(f"Áreas productivas: {agente.areas_productivas}")
            print(
                f"Posiciones en memoria: {len(agente.memoria_comida)}"
            )

        if len(entorno.comida) == 0:
            print("¡ÉXITO! Toda la comida ha sido recolectada.")
            break
        if agente.energia <= 0:
            print("¡AGOTADO! El agente se quedó sin energía.")
            break

    print("\n" + "=" * 50)
    print("SIMULACIÓN COMPLETADA")
    print("=" * 50)
    estadisticas.mostrar_resumen([agente])

    print("\nMétricas específicas Ejercicio 5:")
    print(f"Áreas productivas identificadas: {len(agente.areas_productivas)}")
    print(f"Posiciones memorizadas: {len(agente.memoria_comida)}")

    if agente.memoria_comida:
        posiciones_con_comida = sum(
            1 for freq in agente.memoria_comida.values() if freq > 0
        )
        precision = (
            posiciones_con_comida / len(agente.memoria_comida) * 100
        )
        print(f"Precisión de memoria: {precision:.1f}%")

    if entorno.tiempo > 0:
        eficiencia_busqueda = (
            agente.comida_recolectada / entorno.tiempo * 100
        )
        print(f"Eficiencia de búsqueda: {eficiencia_busqueda:.1f}%")

    # Guardar memoria de áreas para la próxima ejecución
    if hasattr(agente, "guardar_memoria_areas"):
        agente.guardar_memoria_areas()
        print("Memoria de áreas productivas guardada para futuras ejecuciones.")

    try:
        estadisticas.graficar("Ejercicio 5 - Memoria espacial")
    except Exception as e:
        print(f"No se pudo graficar: {e}")


if __name__ == "__main__":
    simular_ejercicio5()
