# src/interfaz/ui_ejercicio2.py
import tkinter as tk

from src.entornos.entorno_limpieza import EntornoLimpiezaConTipos
from src.agentes.agente_limpieza import AgenteLimpiezaConTipos
from src.config.parametros import CONFIG_EJERCICIO_2
from src.interfaz.gui_base import LimpiezaGUI


class Ejercicio2GUI(LimpiezaGUI):
    def __init__(self, root: tk.Tk):
        config = CONFIG_EJERCICIO_2
        entorno = EntornoLimpiezaConTipos(
            config["ancho_grid"], config["alto_grid"], config["num_suciedad"]
        )
        agente = AgenteLimpiezaConTipos(*config["posicion_agente"])
        entorno.agregar_agente(agente)

        super().__init__(root, entorno, agente, "Ejercicio 2 - Tipos de suciedad")
        self.max_pasos = config["max_pasos"]
        self._log("Leyenda: P=Polvo, M=Mancha, B=Barro")
        self._log(f"Configuración: {config}")

    def realizar_paso(self) -> bool:
        if not self.agente.activo or self.agente.energia <= 0:
            self._log("El agente está inactivo o sin energía.")
            return True

        self.entorno.ejecutar_paso()
        self.paso_actual += 1

        self._dibujar_grid()
        self._log(
            f"Paso {self.paso_actual}: pos=({self.agente.x},{self.agente.y}), "
            f"suciedad_limpiada={self.agente.suciedad_limpiada}, "
            f"puntos_totales={self.agente.puntos_totales}"
        )

        if len(self.entorno.suciedad) == 0:
            self._log("¡ÉXITO! Toda la suciedad ha sido limpiada.")
            return True

        if self.max_pasos is not None and self.paso_actual >= self.max_pasos:
            self._log("Se alcanzó el número máximo de pasos.")
            return True

        return False

    def mostrar_resumen(self):
        self._log("\n=== RESUMEN EJERCICIO 2 ===")
        self._log(f"Suciedad limpiada: {self.agente.suciedad_limpiada}")
        self._log(f"Puntos totales: {self.agente.puntos_totales}")
        self._log("Puntos por tipo de suciedad:")
        for tipo, cantidad in self.agente.tipos_limpiados.items():
            valor = self.entorno.tipos_suciedad[tipo]["valor"]
            puntos = cantidad * valor
            self._log(f"  {tipo}: {cantidad} × {valor} = {puntos}")


def lanzar_ui_ejercicio2():
    root = tk.Tk()
    Ejercicio2GUI(root)
    root.mainloop()


if __name__ == "__main__":
    lanzar_ui_ejercicio2()
