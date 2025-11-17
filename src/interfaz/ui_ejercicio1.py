# src/interfaz/ui_ejercicio1.py
import tkinter as tk

from src.entornos.entorno_limpieza import EntornoLimpieza
from src.agentes.agente_limpieza import AgenteLimpiezaConMemoria
from src.config.parametros import CONFIG_EJERCICIO_1
from src.interfaz.gui_base import LimpiezaGUI


def lanzar_ui_ejercicio1():
    config = CONFIG_EJERCICIO_1

    entorno = EntornoLimpieza(
        config["ancho_grid"], config["alto_grid"], config["num_suciedad"]
    )
    agente = AgenteLimpiezaConMemoria(*config["posicion_agente"])
    entorno.agregar_agente(agente)

    root = tk.Tk()
    gui = LimpiezaGUI(root, entorno, agente, titulo="Ejercicio 1 - Limpieza con memoria")
    root.mainloop()


if __name__ == "__main__":
    lanzar_ui_ejercicio1()
