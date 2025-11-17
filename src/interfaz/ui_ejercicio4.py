# src/interfaz/ui_ejercicio4.py
import tkinter as tk
import random

from src.entornos.entorno_recoleccion import EntornoRecoleccion
from src.agentes.agente_recolector import AgenteRecolectorComunicativo
from src.config.parametros import CONFIG_EJERCICIO_4
from src.interfaz.gui_base import RecoleccionGUI


def crear_modelo_desde_usuario():
    base = CONFIG_EJERCICIO_4
    print("Configuración GUI Ejercicio 4 (si dejas vacío, usa los valores por defecto).")
    try:
        num_agentes = int(
            input(f"Nº de agentes [{base['num_agentes']}]: ") or base["num_agentes"]
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
        print("Entrada inválida. Usando configuración por defecto.")
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

    return entorno, agentes


def lanzar_ui_ejercicio4():
    entorno, agentes = crear_modelo_desde_usuario()

    root = tk.Tk()
    gui = RecoleccionGUI(root, entorno, agentes, titulo="Ejercicio 4 - Comunicación recolectores")
    root.mainloop()


if __name__ == "__main__":
    lanzar_ui_ejercicio4()
