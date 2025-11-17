# src/interfaz/ui_ejercicio3.py
import tkinter as tk

from src.entornos.entorno_limpieza import EntornoLimpiezaConObstaculos
from src.agentes.agente_limpieza import AgenteLimpiezaConEvasion
from src.config.parametros import CONFIG_EJERCICIO_3
from src.interfaz.gui_base import LimpiezaGUI


class Ejercicio3GUI(LimpiezaGUI):
    def __init__(self, root: tk.Tk):
        config = CONFIG_EJERCICIO_3
        entorno = EntornoLimpiezaConObstaculos(
            config["ancho_grid"],
            config["alto_grid"],
            config["num_suciedad"],
            config["num_obstaculos"],
        )
        agente = AgenteLimpiezaConEvasion(*config["posicion_agente"])
        entorno.agregar_agente(agente)

        super().__init__(root, entorno, agente, "Ejercicio 3 - Evasión de obstáculos")
        self.max_pasos = config["max_pasos"]
        self._log("Leyenda: A=Agente, X=Obstáculo, *=Suciedad")
        self._log(f"Configuración: {config}")

    def realizar_paso(self) -> bool:
        if not self.agente.activo or self.agente.energia <= 0:
            self._log("El agente está inactivo o sin energía.")
            return True

        self.entorno.ejecutar_paso()
        self.paso_actual += 1

        self._dibujar_grid()

        self._log(f"--- Paso {self.paso_actual} ---")
        self._log("# El agente escanea en un radio de 1 casilla")
        self._log("Obstáculos detectados en el último escaneo:")
        for info in self.agente.ultimo_scan:
            simbolo = "🧱" if info["obstaculo"] else "✅ Libre"
            self._log(
                f"- {info['direccion'].capitalize()}: {info['pos']} → {simbolo}"
            )

        self._log(
            f"Pos=({self.agente.x},{self.agente.y}), "
            f"suciedad_limpiada={self.agente.suciedad_limpiada}, "
            f"energia={self.agente.energia}"
        )

        if len(self.entorno.suciedad) == 0:
            self._log("¡ÉXITO! Toda la suciedad ha sido limpiada.")
            return True

        if self.agente.energia <= 0:
            self._log("¡AGOTADO! El agente se quedó sin energía.")
            return True

        if self.max_pasos is not None and self.paso_actual >= self.max_pasos:
            self._log("Se alcanzó el número máximo de pasos.")
            return True

        return False

    def mostrar_resumen(self):
        config = CONFIG_EJERCICIO_3
        celdas_accesibles = (
            config["ancho_grid"] * config["alto_grid"] - config["num_obstaculos"]
        )
        if celdas_accesibles > 0:
            eficiencia = (
                len(getattr(self.agente, "historial_movimientos", []))
                / celdas_accesibles
                * 100
            )
        else:
            eficiencia = 0

        self._log("\n=== RESUMEN EJERCICIO 3 ===")
        self._log(f"Obstáculos en el entorno: {config['num_obstaculos']}")
        self._log(f"Obstáculos detectados: {len(self.agente.obstaculos_detectados)}")
        self._log(f"Eficiencia de navegación (aprox): {eficiencia:.1f}%")
        self._log(f"Pasos ejecutados: {self.paso_actual}")


def lanzar_ui_ejercicio3():
    root = tk.Tk()
    Ejercicio3GUI(root)
    root.mainloop()


if __name__ == "__main__":
    lanzar_ui_ejercicio3()
