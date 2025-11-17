# simulaciones/sim_ejercicio2.py
from src.agentes.agente_limpieza import AgenteLimpiezaConTipos
from src.entornos.entorno_limpieza import EntornoLimpiezaConTipos
from src.utils.visualizacion import Visualizador
from src.utils.estadisticas import EstadisticasLimpieza
from src.config.parametros import CONFIG_EJERCICIO_2


def simular_ejercicio2():
    """Ejecuta la simulación del ejercicio 2."""
    print("=== EJERCICIO 2: TIPOS DE SUCIEDAD CON VALORES ===")
    print("Objetivo: Agregar diferentes tipos de suciedad con distintos valores.\n")

    config = CONFIG_EJERCICIO_2

    # Opción: permitir al usuario cambiar valores
    print("Valores por defecto: polvo=1, mancha=2, barro=3.")
    resp = input("¿Desea cambiar los valores? (s/n) [n]: ").strip().lower() or "n"

    tipos = None
    if resp == "s":
        try:
            v_polvo = int(input("Valor para POLVO [1]: ") or 1)
            v_mancha = int(input("Valor para MANCHA [2]: ") or 2)
            v_barro = int(input("Valor para BARRO [3]: ") or 3)
            tipos = {
                "polvo": {"valor": v_polvo, "simbolo": "P"},
                "mancha": {"valor": v_mancha, "simbolo": "M"},
                "barro": {"valor": v_barro, "simbolo": "B"},
            }
        except ValueError:
            print("Valores inválidos, usando configuración por defecto.")

    entorno = EntornoLimpiezaConTipos(
        config["ancho_grid"], config["alto_grid"], config["num_suciedad"], tipos
    )

    agente = AgenteLimpiezaConTipos(*config["posicion_agente"])
    estadisticas = EstadisticasLimpieza()
    visualizador = Visualizador()

    entorno.agregar_agente(agente)
    estadisticas.iniciar()

    print("Leyenda: P=Polvo, M=Mancha, B=Barro")
    print("Estado inicial del entorno:")
    visualizador.mostrar_entorno_limpieza(entorno, agente)

    for paso in range(config["max_pasos"]):
        entorno.ejecutar_paso()
        estadisticas.registrar_paso(entorno, agente)

        if paso % 5 == 0 or len(entorno.suciedad) == 0:
            print(f"--- Paso {paso + 1} ---")
            visualizador.mostrar_entorno_limpieza(entorno, agente)
            visualizador.mostrar_estadisticas_agente(agente)

        if len(entorno.suciedad) == 0:
            print("¡ÉXITO! Toda la suciedad ha sido limpiada.")
            break

    print("\n" + "=" * 50)
    print("SIMULACIÓN COMPLETADA")
    print("=" * 50)
    estadisticas.mostrar_resumen(agente)

    print("\nMétricas específicas Ejercicio 2:")
    print("Puntos por tipo de suciedad:")
    for tipo, cantidad in agente.tipos_limpiados.items():
        valor = entorno.tipos_suciedad[tipo]["valor"]
        puntos_tipo = cantidad * valor
        print(f"  {tipo}: {cantidad} unidades × {valor}p = {puntos_tipo}p")

    try:
        estadisticas.graficar("Ejercicio 2 - Tipos de suciedad")
    except Exception as e:
        print(f"No se pudo graficar: {e}")


if __name__ == "__main__":
    simular_ejercicio2()
