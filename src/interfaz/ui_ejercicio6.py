# src/interfaz/ui_ejercicio6.py
import tkinter as tk
import tkinter.simpledialog as sd
import random

from src.entornos.entorno_recoleccion import EntornoRecoleccionCompetitivo
from src.agentes.agente_recolector import AgenteCompetitivo
from src.config.parametros import CONFIG_EJERCICIO_6
from src.interfaz.gui_base import RecoleccionGUI


class Ejercicio6GUI(RecoleccionGUI):
    def __init__(self, root: tk.Tk):
        base = CONFIG_EJERCICIO_6

        # Pedir configuración mediante diálogos de Tkinter
        num_agentes = sd.askinteger(
            "Configuración Ejercicio 6",
            f"Nº de agentes (por defecto {base['num_agentes']}):",
            minvalue=1,
            maxvalue=50,
            parent=root,
        )
        if num_agentes is None:
            num_agentes = base["num_agentes"]

        num_comida = sd.askinteger(
            "Configuración Ejercicio 6",
            f"Nº de comida (por defecto {base['num_comida']}):",
            minvalue=1,
            maxvalue=500,
            parent=root,
        )
        if num_comida is None:
            num_comida = base["num_comida"]

        entorno = EntornoRecoleccionCompetitivo(
            base["ancho_grid"],
            base["alto_grid"],
            num_comida,
            base["num_obstaculos"],
        )

        agentes = []
        estrategias = base["estrategias"]
        for i in range(num_agentes):
            x = random.randint(0, base["ancho_grid"] - 1)
            y = random.randint(0, base["alto_grid"] - 1)
            estrategia = estrategias[i] if i < len(estrategias) else "agresiva"
            a = AgenteCompetitivo(x, y, f"{estrategia[0].upper()}{i+1}", estrategia)
            agentes.append(a)
            entorno.agregar_agente(a)

        super().__init__(root, entorno, agentes, "Ejercicio 6 - Competencia por recursos")
        self.max_pasos = base["max_pasos"]
        self._log(
            f"Configuración: agentes={num_agentes}, comida={num_comida}, "
            f"obstáculos={base['num_obstaculos']}"
        )

    def realizar_paso(self) -> bool:
        self.entorno.ejecutar_paso()
        self.paso_actual += 1

        self._dibujar_grid()

        self._log(f"--- Paso {self.paso_actual} ---")
        for a in self.agentes:
            conflictos = a.conflictos_ganados + a.conflictos_perdidos
            self._log(
                f"{a.id} ({a.estrategia}): pos=({a.x},{a.y}), comida={a.comida_recolectada}, "
                f"energia={a.energia}, conflictos={conflictos}"
            )

        if len(self.entorno.comida) == 0 and self.paso_actual > 5:
            self._log("¡RECURSOS AGOTADOS! No queda comida en el entorno.")
            return True

        if self.max_pasos is not None and self.paso_actual >= self.max_pasos:
            self._log("Se alcanzó el número máximo de pasos.")
            return True

        return False

    def mostrar_resumen(self):
        self._log("\n=== RESUMEN EJERCICIO 6 ===")

        if self.agentes:
            ganador = max(self.agentes, key=lambda a: a.comida_recolectada)
            self._log(
                f"🏆 GANADOR: {ganador.id} con {ganador.comida_recolectada} unidades de comida "
                f"(estrategia: {ganador.estrategia})"
            )

        estrategias_dict = {}
        for a in self.agentes:
            estrategias_dict.setdefault(a.estrategia, []).append(a)

        for estrategia, grupo in estrategias_dict.items():
            comida_total = sum(a.comida_recolectada for a in grupo)
            conflictos_total = sum(
                a.conflictos_ganados + a.conflictos_perdidos for a in grupo
            )
            self._log(f"\nEstrategia {estrategia.upper()}:")
            self._log(f"  Agentes: {len(grupo)}")
            self._log(f"  Comida total: {comida_total}")
            self._log(f"  Conflictos totales: {conflictos_total}")
            if conflictos_total > 0:
                ratio = (
                    sum(a.conflictos_ganados for a in grupo)
                    / conflictos_total
                    * 100
                )
                self._log(f"  Ratio de conflictos ganados: {ratio:.1f}%")

        self._log(f"\nPasos ejecutados: {self.paso_actual}")


def lanzar_ui_ejercicio6():
    root = tk.Tk()
    Ejercicio6GUI(root)
    root.mainloop()


if __name__ == "__main__":
    lanzar_ui_ejercicio6()
