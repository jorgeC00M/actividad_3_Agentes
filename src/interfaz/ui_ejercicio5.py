# src/interfaz/ui_ejercicio5.py
import tkinter as tk
import tkinter.simpledialog as sd
import random

from src.entornos.entorno_recoleccion import EntornoRecoleccion
from src.agentes.agente_recolector import AgenteRecolectorConAprendizaje
from src.config.parametros import CONFIG_EJERCICIO_5
from src.interfaz.gui_base import RecoleccionGUI


def distribuir_comida_por_areas(entorno, base_num: int):
    """
    Divide el grid en 4 áreas y distribuye comida:
    Área 3 > Área 1 > Área 2 > Área 4.
    """
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


class Ejercicio5GUI(RecoleccionGUI):
    def __init__(self, root: tk.Tk):
        config = CONFIG_EJERCICIO_5

        # Preguntar al usuario por GUI la cantidad de pasos
        max_pasos = sd.askinteger(
            "Configuración Ejercicio 5",
            f"Máximo de pasos para el agente (por defecto {config['max_pasos']}):",
            minvalue=1,
            maxvalue=500,
            parent=root,
        )
        if max_pasos is None:
            max_pasos = config["max_pasos"]

        entorno = EntornoRecoleccion(
            config["ancho_grid"],
            config["alto_grid"],
            config["num_comida"],
            config["num_obstaculos"],
        )

        distribuir_comida_por_areas(entorno, config["num_comida"])

        agente = AgenteRecolectorConAprendizaje(*config["posicion_agente"], "Aprendiz")
        entorno.agregar_agente(agente)
        agentes = [agente]

        super().__init__(root, entorno, agentes, "Ejercicio 5 - Memoria espacial")
        self.max_pasos = max_pasos
        self.agente = agente
        self._log(f"Configuración base: {config}")
        self._log(f"Máximo de pasos asignado por el usuario: {max_pasos}")
        self._log(
            "Nota: en ejecuciones sucesivas, el agente reutiliza memoria de áreas productivas (archivo JSON)."
        )

    def realizar_paso(self) -> bool:
        self.entorno.ejecutar_paso()
        self.paso_actual += 1

        self._dibujar_grid()

        a = self.agente
        self._log(
            f"Paso {self.paso_actual}: pos=({a.x},{a.y}), comida={a.comida_recolectada}, "
            f"energia={a.energia}, areas_productivas={a.areas_productivas}"
        )

        if len(self.entorno.comida) == 0:
            self._log("¡ÉXITO! Toda la comida ha sido recolectada.")
            return True

        if a.energia <= 0:
            self._log("¡AGOTADO! El agente se quedó sin energía.")
            return True

        if self.max_pasos is not None and self.paso_actual >= self.max_pasos:
            self._log("Se alcanzó el número máximo de pasos.")
            return True

        return False

    def mostrar_resumen(self):
        a = self.agente
        self._log("\n=== RESUMEN EJERCICIO 5 ===")
        self._log(f"Comida recolectada: {a.comida_recolectada}")
        self._log(f"Áreas productivas identificadas: {len(a.areas_productivas)}")
        self._log(f"Posiciones memorizadas: {len(a.memoria_comida)}")

        if a.memoria_comida:
            posiciones_con_comida = sum(
                1 for freq in a.memoria_comida.values() if freq > 0
            )
            precision = (
                posiciones_con_comida / len(a.memoria_comida) * 100
            )
            self._log(f"Precisión de memoria: {precision:.1f}%")

        if self.paso_actual > 0:
            eficiencia = a.comida_recolectada / self.paso_actual * 100
            self._log(f"Eficiencia de búsqueda: {eficiencia:.1f}%")

        try:
            a.guardar_memoria_areas()
            self._log("Memoria de áreas productivas guardada para futuras ejecuciones.")
        except Exception:
            pass


def lanzar_ui_ejercicio5():
    root = tk.Tk()
    Ejercicio5GUI(root)
    root.mainloop()


if __name__ == "__main__":
    lanzar_ui_ejercicio5()
