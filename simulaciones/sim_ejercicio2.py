# simulaciones/sim_ejercicio2.py
import time

from src.entornos.entorno_limpieza import EntornoLimpiezaConTipos
from src.agentes.agente_limpieza import AgenteLimpiezaConTipos
from src.config.parametros import CONFIG_EJERCICIO_2
from src.utils.visualizacion import Visualizador
from src.utils.estadisticas import EstadisticasLimpieza


def simular_ejercicio2():
    print("=== EJERCICIO 2 (CONSOLa) - TIPOS DE SUCIEDAD CON VALORES ===")
    print("Objetivo: Agregar diferentes tipos de suciedad con distintos puntajes.\n")

    config = CONFIG_EJERCICIO_2
    entorno = EntornoLimpiezaConTipos(
        config["ancho_grid"], config["alto_grid"], config["num_suciedad"]
    )
    agente = AgenteLimpiezaConTipos(*config["posicion_agente"])
    entorno.agregar_agente(agente)

    vis = Visualizador()
    stats = EstadisticasLimpieza()
    stats.iniciar()

    print("Leyenda: P=Polvo(1p), M=Mancha(2p), B=Barro(3p)")
    print("Estado inicial del entorno:")
    vis.mostrar_entorno_limpieza(entorno, agente)

    for paso in range(1, config["max_pasos"] + 1):
        entorno.ejecutar_paso()
        stats.registrar_paso(entorno, agente)

        print(f"\n--- Paso {paso} ---")
        vis.mostrar_entorno_limpieza(entorno, agente)
        print(
            f"Pos: ({agente.x},{agente.y}) | Energía: {agente.energia} | "
            f"Suciedad limpiada: {agente.suciedad_limpiada} | Puntos: {agente.puntos_totales}"
        )

        if len(entorno.suciedad) == 0:
            print("\n¡ÉXITO! Toda la suciedad ha sido limpiada.")
            break

        time.sleep(0.1)

    print("\n=== RESULTADOS FINALES EJERCICIO 2 ===")
    stats.mostrar_resumen(agente)
    print("Puntos por tipo de suciedad:")
    for tipo, cantidad in agente.tipos_limpiados.items():
        valor = entorno.tipos_suciedad[tipo]["valor"]
        puntos = cantidad * valor
        print(f"  {tipo}: {cantidad} × {valor} = {puntos}")

    print(f"Pasos ejecutados: {entorno.tiempo}")


if __name__ == "__main__":
    simular_ejercicio2()
