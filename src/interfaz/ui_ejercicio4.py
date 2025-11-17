# src/interfaz/ui_ejercicio4.py
import tkinter as tk
import random

from src.entornos.entorno_recoleccion import EntornoRecoleccion
from src.agentes.agente_recolector import AgenteRecolectorComunicativo
from src.config.parametros import CONFIG_EJERCICIO_4
from src.interfaz.gui_base import RecoleccionGUI


class Ejercicio4GUI(RecoleccionGUI):
    def __init__(self, root: tk.Tk):
        config = CONFIG_EJERCICIO_4

        print("Configuración Ejercicio 4 (dejar vacío usa por defecto):")
        try:
            num_agentes = int(
                input(f"Nº de agentes [{config['num_agentes']}]: ")
                or config["num_agentes"]
            )
            num_comida = int(
                input(f"Nº de comida [{config['num_comida']}]: ")
                or config["num_comida"]
            )
            num_obst = int(
                input(f"Nº de obstáculos [{config['num_obstaculos']}]: ")
                or config["num_obstaculos"]
            )
        except ValueError:
            num_agentes = config["num_agentes"]
            num_comida = config["num_comida"]
            num_obst = config["num_obstaculos"]

        entorno = EntornoRecoleccion(
            config["ancho_grid"], config["alto_grid"], num_comida, num_obst
        )

        agentes = []
        for i in range(num_agentes):
            x = random.randint(0, config["ancho_grid"] - 1)
            y = random.randint(0, config["alto_grid"] - 1)
            a = AgenteRecolectorComunicativo(x, y, f"R{i+1}")
            agentes.append(a)
            entorno.agregar_agente(a)

        super().__init__(root, entorno, agentes, "Ejercicio 4 - Comunicación recolectores")
        self.max_pasos = config["max_pasos"]
        self._log(
            f"Configuración: agentes={num_agentes}, comida={num_comida}, obstáculos={num_obst}"
        )

    def realizar_paso(self) -> bool:
        for agente in self.agentes:
            comida_local = agente.percibir(self.entorno)
            otros = [a for a in self.agentes if a.id != agente.id]
            if comida_local and otros:
                for pos in comida_local[:2]:
                    agente.enviar_mensaje(otros, "comida_encontrada", pos)
                    agente.enviar_mensaje(otros, "objetivo_reservado", pos)

        self.entorno.ejecutar_paso()
        self.paso_actual += 1

        self._dibujar_grid()

        self._log(f"--- Paso {self.paso_actual} ---")
        for a in self.agentes:
            self._log(
                f"{a.id}: pos=({a.x},{a.y}), comida={a.comida_recolectada}, "
                f"energia={a.energia}, objetivos_reservados={list(a.objetivos_reservados)}"
            )

        if len(self.entorno.comida) == 0:
            self._log("¡ÉXITO! Toda la comida ha sido recolectada.")
            return True

        if self.max_pasos is not None and self.paso_actual >= self.max_pasos:
            self._log("Se alcanzó el número máximo de pasos.")
            return True

        return False

    def mostrar_resumen(self):
        self._log("\n=== RESUMEN EJERCICIO 4 ===")
        comida_total = sum(a.comida_recolectada for a in self.agentes)
        total_mensajes = sum(getattr(a, "mensajes_enviados", 0) for a in self.agentes)
        total_obj_res = sum(len(a.objetivos_reservados) for a in self.agentes)

        self._log(f"Comida total recolectada: {comida_total}")
        self._log(f"Mensajes enviados totales: {total_mensajes}")
        self._log(f"Objetivos reservados totales: {total_obj_res}")

        if self.paso_actual > 0 and len(self.agentes) > 0:
            eficiencia = comida_total / (self.paso_actual * len(self.agentes))
            self._log(
                f"Eficiencia de coordinación: {eficiencia:.3f} comida/(paso·agente)"
            )


def lanzar_ui_ejercicio4():
    root = tk.Tk()
    Ejercicio4GUI(root)
    root.mainloop()


if __name__ == "__main__":
    lanzar_ui_ejercicio4()
