# src/interfaz/gui_base.py
import tkinter as tk
from tkinter import ttk
from typing import List, Optional, Callable

from src.utils.visualizacion import Visualizador  # por si quieres debug extra


CELL_SIZE = 40  # tamaño de cada celda en píxeles
AUTO_DELAY_MS = 300  # retardo entre pasos automáticos


class LimpiezaGUI:
    """GUI genérica para entornos de limpieza (Ej.1–3)."""

    def __init__(self, root: tk.Tk, entorno, agente, titulo: str = "Simulación Limpieza"):
        self.root = root
        self.entorno = entorno
        self.agente = agente
        self.titulo = titulo

        self.running = False  # modo auto
        self.paso_actual = 0

        self._build_ui()

    def _build_ui(self):
        self.root.title(self.titulo)

        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Canvas para el grid
        width_px = self.entorno.ancho * CELL_SIZE
        height_px = self.entorno.alto * CELL_SIZE
        self.canvas = tk.Canvas(main_frame, width=width_px, height=height_px, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=3)

        # Panel de control
        control_frame = ttk.Frame(main_frame, padding=(10, 0, 0, 0))
        control_frame.grid(row=0, column=1, sticky="nw")

        self.lbl_paso = ttk.Label(control_frame, text="Paso: 0")
        self.lbl_paso.grid(row=0, column=0, sticky="w")

        self.lbl_suciedad = ttk.Label(control_frame, text="Suciedad restante: ?")
        self.lbl_suciedad.grid(row=1, column=0, sticky="w")

        self.lbl_energia = ttk.Label(control_frame, text="Energía agente: ?")
        self.lbl_energia.grid(row=2, column=0, sticky="w")

        self.lbl_extra = ttk.Label(control_frame, text="", wraplength=250)
        self.lbl_extra.grid(row=3, column=0, sticky="w", pady=(10, 0))

        # Botones
        btn_frame = ttk.Frame(control_frame, padding=(0, 10, 0, 0))
        btn_frame.grid(row=4, column=0, sticky="w")

        self.btn_paso = ttk.Button(btn_frame, text="Paso", command=self.step_once)
        self.btn_paso.grid(row=0, column=0, padx=5)

        self.btn_auto = ttk.Button(btn_frame, text="Auto ▶", command=self.toggle_auto)
        self.btn_auto.grid(row=0, column=1, padx=5)

        self.btn_reset = ttk.Button(btn_frame, text="Reset", command=self.reset)
        self.btn_reset.grid(row=0, column=2, padx=5)

        self._draw_grid()

    def _draw_grid(self):
        self.canvas.delete("all")
        ancho, alto = self.entorno.ancho, self.entorno.alto

        for y in range(alto):
            for x in range(ancho):
                x0 = x * CELL_SIZE
                y0 = y * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE

                fill = "white"

                # Obstáculos si el entorno los tiene
                if hasattr(self.entorno, "obstaculos") and (x, y) in getattr(
                    self.entorno, "obstaculos", set()
                ):
                    fill = "gray"

                # Suciedad
                if hasattr(self.entorno, "suciedad"):
                    s = self.entorno.suciedad
                    if isinstance(s, dict):
                        if (x, y) in s:
                            fill = "sandybrown"
                    elif (x, y) in s:
                        fill = "sandybrown"

                # Celdas visitadas (solo para agentes con memoria)
                if hasattr(self.agente, "lugares_visitados"):
                    if (x, y) in self.agente.lugares_visitados:
                        fill = "lightblue"

                self.canvas.create_rectangle(
                    x0, y0, x1, y1, fill=fill, outline="black"
                )

        # Dibujar agente
        ax, ay = self.agente.x, self.agente.y
        x0 = ax * CELL_SIZE + 5
        y0 = ay * CELL_SIZE + 5
        x1 = x0 + CELL_SIZE - 10
        y1 = y0 + CELL_SIZE - 10
        self.canvas.create_oval(x0, y0, x1, y1, fill="blue", outline="black")

        self._update_labels()

    def _update_labels(self):
        self.lbl_paso.config(text=f"Paso: {self.paso_actual}")
        self.lbl_suciedad.config(text=f"Suciedad restante: {len(self.entorno.suciedad)}")
        self.lbl_energia.config(text=f"Energía agente: {self.agente.energia}")

        extra = []
        if hasattr(self.agente, "suciedad_limpiada"):
            extra.append(f"Suciedad limpiada: {self.agente.suciedad_limpiada}")
        if hasattr(self.agente, "puntos_totales"):
            extra.append(f"Puntos totales: {self.agente.puntos_totales}")
        if hasattr(self.agente, "obstaculos_detectados"):
            extra.append(f"Obstáculos detectados: {len(self.agente.obstaculos_detectados)}")

        self.lbl_extra.config(text="\n".join(extra))

    def step_once(self):
        if not self.agente.activo or self.agente.energia <= 0:
            return
        self.entorno.ejecutar_paso()
        self.paso_actual += 1
        self._draw_grid()

    def toggle_auto(self):
        self.running = not self.running
        self.btn_auto.config(text="Auto ⏸" if self.running else "Auto ▶")
        if self.running:
            self._auto_loop()

    def _auto_loop(self):
        if not self.running:
            return
        self.step_once()
        if self.agente.activo and self.agente.energia > 0 and len(self.entorno.suciedad) > 0:
            self.root.after(AUTO_DELAY_MS, self._auto_loop)
        else:
            self.running = False
            self.btn_auto.config(text="Auto ▶")

    def reset(self):
        # Por simplicidad, solo paramos auto; el reinicio completo lo dejas a nivel de UI específica
        self.running = False
        self.btn_auto.config(text="Auto ▶")


class RecoleccionGUI:
    """GUI genérica para entornos de recolección (Ej.4–6)."""

    def __init__(self, root: tk.Tk, entorno, agentes: List, titulo: str = "Simulación Recolección"):
        self.root = root
        self.entorno = entorno
        self.agentes = agentes
        self.titulo = titulo

        self.running = False
        self.paso_actual = 0

        self._build_ui()

    def _build_ui(self):
        self.root.title(self.titulo)

        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")

        width_px = self.entorno.ancho * CELL_SIZE
        height_px = self.entorno.alto * CELL_SIZE
        self.canvas = tk.Canvas(main_frame, width=width_px, height=height_px, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=4)

        control_frame = ttk.Frame(main_frame, padding=(10, 0, 0, 0))
        control_frame.grid(row=0, column=1, sticky="nw")

        self.lbl_paso = ttk.Label(control_frame, text="Paso: 0")
        self.lbl_paso.grid(row=0, column=0, sticky="w")

        self.lbl_comida = ttk.Label(control_frame, text="Comida restante: ?")
        self.lbl_comida.grid(row=1, column=0, sticky="w")

        self.lbl_agentes = ttk.Label(control_frame, text="Agentes: ?")
        self.lbl_agentes.grid(row=2, column=0, sticky="w")

        self.lbl_extra = ttk.Label(control_frame, text="", wraplength=280)
        self.lbl_extra.grid(row=3, column=0, sticky="w", pady=(10, 0))

        # Botones
        btn_frame = ttk.Frame(control_frame, padding=(0, 10, 0, 0))
        btn_frame.grid(row=4, column=0, sticky="w")

        self.btn_paso = ttk.Button(btn_frame, text="Paso", command=self.step_once)
        self.btn_paso.grid(row=0, column=0, padx=5)

        self.btn_auto = ttk.Button(btn_frame, text="Auto ▶", command=self.toggle_auto)
        self.btn_auto.grid(row=0, column=1, padx=5)

        self.btn_reset = ttk.Button(btn_frame, text="Reset", command=self.reset)
        self.btn_reset.grid(row=0, column=2, padx=5)

        # Área de log simple
        log_frame = ttk.Frame(main_frame, padding=(10, 10, 0, 0))
        log_frame.grid(row=1, column=1, sticky="nw")

        ttk.Label(log_frame, text="Log de comunicación / estado:", anchor="w").grid(
            row=0, column=0, sticky="w"
        )
        self.txt_log = tk.Text(log_frame, width=40, height=15, state="disabled")
        self.txt_log.grid(row=1, column=0, sticky="nsew")

        self._draw_grid()

    def _log(self, texto: str):
        self.txt_log.config(state="normal")
        self.txt_log.insert("end", texto + "\n")
        self.txt_log.see("end")
        self.txt_log.config(state="disabled")

    def _draw_grid(self):
        self.canvas.delete("all")
        ancho, alto = self.entorno.ancho, self.entorno.alto

        for y in range(alto):
            for x in range(ancho):
                x0 = x * CELL_SIZE
                y0 = y * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE

                fill = "white"

                # Obstáculos
                if (x, y) in self.entorno.obstaculos:
                    fill = "gray"

                # Comida
                if (x, y) in self.entorno.comida:
                    fill = "lightgreen"

                self.canvas.create_rectangle(
                    x0, y0, x1, y1, fill=fill, outline="black"
                )

        # Agentes
        for a in self.agentes:
            ax, ay = a.x, a.y
            x0 = ax * CELL_SIZE + 5
            y0 = ay * CELL_SIZE + 5
            x1 = x0 + CELL_SIZE - 10
            y1 = y0 + CELL_SIZE - 10
            self.canvas.create_oval(x0, y0, x1, y1, fill="blue", outline="black")
            self.canvas.create_text(
                ax * CELL_SIZE + CELL_SIZE / 2,
                ay * CELL_SIZE + CELL_SIZE / 2,
                text=a.id,
                fill="white",
                font=("Arial", 8, "bold"),
            )

        self._update_labels()

    def _update_labels(self):
        self.lbl_paso.config(text=f"Paso: {self.paso_actual}")
        self.lbl_comida.config(text=f"Comida restante: {len(self.entorno.comida)}")
        self.lbl_agentes.config(text=f"Agentes: {len(self.agentes)}")

        # Extra: comida total y conflictos si existen
        comida_total = sum(getattr(a, "comida_recolectada", 0) for a in self.agentes)
        conflictos = sum(
            getattr(a, "conflictos_ganados", 0) + getattr(a, "conflictos_perdidos", 0)
            for a in self.agentes
        )
        self.lbl_extra.config(
            text=f"Comida total recolectada: {comida_total}\nConflictos acumulados: {conflictos}"
        )

    def step_once(self):
        self.entorno.ejecutar_paso()
        self.paso_actual += 1
        self._draw_grid()

        # Log simple de estado de agentes
        for a in self.agentes:
            self._log(
                f"[Paso {self.paso_actual}] {a.id}: pos=({a.x},{a.y}), comida={a.comida_recolectada}, energía={a.energia}"
            )

    def toggle_auto(self):
        self.running = not self.running
        self.btn_auto.config(text="Auto ⏸" if self.running else "Auto ▶")
        if self.running:
            self._auto_loop()

    def _auto_loop(self):
        if not self.running:
            return
        self.step_once()
        if len(self.entorno.comida) > 0 and any(a.energia > 0 for a in self.agentes):
            self.root.after(AUTO_DELAY_MS, self._auto_loop)
        else:
            self.running = False
            self.btn_auto.config(text="Auto ▶")

    def reset(self):
        self.running = False
        self.btn_auto.config(text="Auto ▶")
        # Igual que antes: reinicio completo del modelo se hace desde las UIs específicas
