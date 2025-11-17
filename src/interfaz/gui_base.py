# src/interfaz/gui_base.py
import tkinter as tk
from tkinter import ttk
from typing import List, Optional

CELL_SIZE = 40
AUTO_DELAY_MS = 200  # ms entre pasos en modo auto


class BaseGUI:
    """Clase base para GUIs de simulación."""

    def __init__(self, root: tk.Tk, titulo: str):
        self.root = root
        self.root.title(titulo)
        self.running = False
        self.paso_actual = 0
        self.max_pasos: Optional[int] = None

    def _log(self, texto: str):
        self.txt_log.config(state="normal")
        self.txt_log.insert("end", texto + "\n")
        self.txt_log.see("end")
        self.txt_log.config(state="disabled")

    def _toggle_auto(self):
        self.running = not self.running
        self.btn_auto.config(text="Auto ⏸" if self.running else "Auto ▶")
        if self.running:
            self._auto_loop()

    def _auto_loop(self):
        if not self.running:
            return
        if self.max_pasos is not None and self.paso_actual >= self.max_pasos:
            self.running = False
            self.btn_auto.config(text="Auto ▶")
            return

        terminado = self.realizar_paso()
        if not terminado:
            self.root.after(AUTO_DELAY_MS, self._auto_loop)
        else:
            self.running = False
            self.btn_auto.config(text="Auto ▶")

    def realizar_paso(self) -> bool:
        raise NotImplementedError

    def mostrar_resumen(self):
        raise NotImplementedError


class LimpiezaGUI(BaseGUI):
    """GUI genérica para un entorno de limpieza con un solo agente."""

    def __init__(self, root: tk.Tk, entorno, agente, titulo: str):
        super().__init__(root, titulo)
        self.entorno = entorno
        self.agente = agente

        self._build_ui()
        self._dibujar_grid()
        self._log("Simulación de limpieza lista. Use 'Paso' o 'Auto' para avanzar.")

    def _build_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")

        width_px = self.entorno.ancho * CELL_SIZE
        height_px = self.entorno.alto * CELL_SIZE

        self.canvas = tk.Canvas(main_frame, width=width_px, height=height_px, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=3)

        side = ttk.Frame(main_frame, padding=(10, 0, 0, 0))
        side.grid(row=0, column=1, sticky="n")

        self.lbl_paso = ttk.Label(side, text="Paso: 0")
        self.lbl_paso.grid(row=0, column=0, sticky="w")

        self.lbl_suciedad = ttk.Label(
            side, text=f"Suciedad restante: {len(self.entorno.suciedad)}"
        )
        self.lbl_suciedad.grid(row=1, column=0, sticky="w")

        self.lbl_energia = ttk.Label(side, text=f"Energía: {self.agente.energia}")
        self.lbl_energia.grid(row=2, column=0, sticky="w")

        self.lbl_extra = ttk.Label(side, text="", wraplength=260)
        self.lbl_extra.grid(row=3, column=0, sticky="w", pady=(10, 0))

        btn_frame = ttk.Frame(side, padding=(0, 10, 0, 0))
        btn_frame.grid(row=4, column=0, sticky="w")

        self.btn_paso = ttk.Button(btn_frame, text="Paso", command=self._on_paso)
        self.btn_paso.grid(row=0, column=0, padx=5)

        self.btn_auto = ttk.Button(btn_frame, text="Auto ▶", command=self._toggle_auto)
        self.btn_auto.grid(row=0, column=1, padx=5)

        self.btn_resumen = ttk.Button(btn_frame, text="Resumen", command=self.mostrar_resumen)
        self.btn_resumen.grid(row=0, column=2, padx=5)

        self.btn_salir = ttk.Button(btn_frame, text="Salir", command=self.root.destroy)
        self.btn_salir.grid(row=0, column=3, padx=5)

        log_frame = ttk.Frame(main_frame, padding=(10, 10, 0, 0))
        log_frame.grid(row=1, column=1, sticky="nsew")

        ttk.Label(log_frame, text="Log / Resultados:", anchor="w").grid(
            row=0, column=0, sticky="w"
        )
        self.txt_log = tk.Text(log_frame, width=45, height=18, state="disabled")
        self.txt_log.grid(row=1, column=0, sticky="nsew")

    def _on_paso(self):
        terminado = self.realizar_paso()
        if terminado:
            self._log("Simulación terminada.")

    def _dibujar_grid(self):
        self.canvas.delete("all")
        for y in range(self.entorno.alto):
            for x in range(self.entorno.ancho):
                x0 = x * CELL_SIZE
                y0 = y * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE

                fill = "white"

                if hasattr(self.entorno, "obstaculos") and (
                    x, y
                ) in getattr(self.entorno, "obstaculos", set()):
                    fill = "gray"

                if hasattr(self.entorno, "suciedad"):
                    s = self.entorno.suciedad
                    if isinstance(s, dict) and (x, y) in s:
                        tipo = s[(x, y)]["tipo"]
                        fill = "sandybrown"
                    elif isinstance(s, set) and (x, y) in s:
                        fill = "sandybrown"

                if hasattr(self.agente, "lugares_visitados"):
                    if (x, y) in self.agente.lugares_visitados:
                        fill = "lightblue"

                self.canvas.create_rectangle(
                    x0, y0, x1, y1, fill=fill, outline="black"
                )

        ax, ay = self.agente.x, self.agente.y
        x0 = ax * CELL_SIZE + 5
        y0 = ay * CELL_SIZE + 5
        x1 = x0 + CELL_SIZE - 10
        y1 = y0 + CELL_SIZE - 10
        self.canvas.create_oval(x0, y0, x1, y1, fill="blue")

        self.lbl_paso.config(text=f"Paso: {self.paso_actual}")
        self.lbl_suciedad.config(text=f"Suciedad restante: {len(self.entorno.suciedad)}")
        self.lbl_energia.config(text=f"Energía: {self.agente.energia}")

        extra = []
        if hasattr(self.agente, "suciedad_limpiada"):
            extra.append(f"Suciedad limpiada: {self.agente.suciedad_limpiada}")
        if hasattr(self.agente, "puntos_totales"):
            extra.append(f"Puntos totales: {self.agente.puntos_totales}")
        if hasattr(self.agente, "obstaculos_detectados"):
            extra.append(f"Obstáculos detectados: {len(self.agente.obstaculos_detectados)}")
        self.lbl_extra.config(text="\n".join(extra))


class RecoleccionGUI(BaseGUI):
    """GUI genérica para un entorno de recolección con múltiples agentes."""

    def __init__(self, root: tk.Tk, entorno, agentes: List, titulo: str):
        super().__init__(root, titulo)
        self.entorno = entorno
        self.agentes = agentes

        self._build_ui()
        self._dibujar_grid()
        self._log("Simulación de recolección lista. Use 'Paso' o 'Auto' para avanzar.")

    def _build_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")

        width_px = self.entorno.ancho * CELL_SIZE
        height_px = self.entorno.alto * CELL_SIZE

        self.canvas = tk.Canvas(main_frame, width=width_px, height=height_px, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=3)

        side = ttk.Frame(main_frame, padding=(10, 0, 0, 0))
        side.grid(row=0, column=1, sticky="n")

        self.lbl_paso = ttk.Label(side, text="Paso: 0")
        self.lbl_paso.grid(row=0, column=0, sticky="w")

        self.lbl_comida = ttk.Label(
            side, text=f"Comida restante: {len(self.entorno.comida)}"
        )
        self.lbl_comida.grid(row=1, column=0, sticky="w")

        self.lbl_agentes = ttk.Label(side, text=f"Agentes: {len(self.agentes)}")
        self.lbl_agentes.grid(row=2, column=0, sticky="w")

        self.lbl_extra = ttk.Label(side, text="", wraplength=260)
        self.lbl_extra.grid(row=3, column=0, sticky="w", pady=(10, 0))

        btn_frame = ttk.Frame(side, padding=(0, 10, 0, 0))
        btn_frame.grid(row=4, column=0, sticky="w")

        self.btn_paso = ttk.Button(btn_frame, text="Paso", command=self._on_paso)
        self.btn_paso.grid(row=0, column=0, padx=5)

        self.btn_auto = ttk.Button(btn_frame, text="Auto ▶", command=self._toggle_auto)
        self.btn_auto.grid(row=0, column=1, padx=5)

        self.btn_resumen = ttk.Button(btn_frame, text="Resumen", command=self.mostrar_resumen)
        self.btn_resumen.grid(row=0, column=2, padx=5)

        self.btn_salir = ttk.Button(btn_frame, text="Salir", command=self.root.destroy)
        self.btn_salir.grid(row=0, column=3, padx=5)

        log_frame = ttk.Frame(main_frame, padding=(10, 10, 0, 0))
        log_frame.grid(row=1, column=1, sticky="nsew")

        ttk.Label(log_frame, text="Log / Resultados:", anchor="w").grid(
            row=0, column=0, sticky="w"
        )
        self.txt_log = tk.Text(log_frame, width=45, height=18, state="disabled")
        self.txt_log.grid(row=1, column=0, sticky="nsew")

    def _on_paso(self):
        terminado = self.realizar_paso()
        if terminado:
            self._log("Simulación terminada.")

    def _dibujar_grid(self):
        self.canvas.delete("all")
        for y in range(self.entorno.alto):
            for x in range(self.entorno.ancho):
                x0 = x * CELL_SIZE
                y0 = y * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE

                fill = "white"
                if (x, y) in getattr(self.entorno, "obstaculos", set()):
                    fill = "gray"
                elif (x, y) in getattr(self.entorno, "comida", {}):
                    fill = "lightgreen"

                self.canvas.create_rectangle(
                    x0, y0, x1, y1, fill=fill, outline="black"
                )

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

        self.lbl_paso.config(text=f"Paso: {self.paso_actual}")
        self.lbl_comida.config(text=f"Comida restante: {len(self.entorno.comida)}")
        self.lbl_agentes.config(text=f"Agentes: {len(self.agentes)}")

        comida_total = sum(getattr(a, "comida_recolectada", 0) for a in self.agentes)
        conflictos = sum(
            getattr(a, "conflictos_ganados", 0) + getattr(a, "conflictos_perdidos", 0)
            for a in self.agentes
        )
        self.lbl_extra.config(
            text=f"Comida total recolectada: {comida_total}\nConflictos acumulados: {conflictos}"
        )
