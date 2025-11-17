# src/utils/estadisticas.py
from typing import Dict, Any, List
import time

import numpy as np
import matplotlib.pyplot as plt


class EstadisticasLimpieza:
    """Recolecta estadísticas para simulaciones de limpieza."""

    def __init__(self):
        self.datos = {
            "tiempos": [],
            "suciedad_limpiada": [],
            "lugares_visitados": [],
            "eficiencia": [],
        }
        self.inicio_tiempo = None

    def iniciar(self):
        """Inicia el contador de tiempo."""
        self.inicio_tiempo = time.time()

    def registrar_paso(self, entorno, agente):
        """Registra datos del paso actual."""
        tiempo_actual = time.time() - self.inicio_tiempo if self.inicio_tiempo else 0

        self.datos["tiempos"].append(tiempo_actual)
        self.datos["suciedad_limpiada"].append(
            getattr(agente, "suciedad_limpiada", 0)
        )
        self.datos["lugares_visitados"].append(
            len(getattr(agente, "lugares_visitados", set()))
        )

        # Calcular eficiencia de cobertura
        total_celdas = entorno.ancho * entorno.alto
        if hasattr(agente, "lugares_visitados"):
            eficiencia = len(agente.lugares_visitados) / total_celdas * 100
            self.datos["eficiencia"].append(eficiencia)

    def mostrar_resumen(self, agente):
        """Muestra resumen de estadísticas."""
        print("=== ESTADÍSTICAS FINALES ===")
        print(f"Suciedad limpiada: {getattr(agente, 'suciedad_limpiada', 0)}")
        print(
            f"Lugares visitados: {len(getattr(agente, 'lugares_visitados', set()))}"
        )

        if hasattr(agente, "puntos_totales"):
            print(f"Puntos totales: {agente.puntos_totales}")

        if hasattr(agente, "tipos_limpiados"):
            print(f"Tipos limpiados: {agente.tipos_limpiados}")

        if self.datos["eficiencia"]:
            print(f"Eficiencia: {self.datos['eficiencia'][-1]:.1f}%")

    def graficar(self, titulo="Evolución de la limpieza"):
        if not self.datos["tiempos"]:
            print("No hay datos para graficar.")
            return

        tiempos = np.array(self.datos["tiempos"])
        suciedad = np.array(self.datos["suciedad_limpiada"])
        eficiencia = (
            np.array(self.datos["eficiencia"])
            if self.datos["eficiencia"]
            else None
        )

        plt.figure()
        plt.plot(tiempos, suciedad, label="Suciedad limpiada")
        if eficiencia is not None:
            plt.plot(
                tiempos[: len(eficiencia)],
                eficiencia,
                linestyle="--",
                label="Eficiencia (%)",
            )
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Valor")
        plt.title(titulo)
        plt.legend()
        plt.grid(True)
        plt.show()


class EstadisticasRecoleccion:
    """Recolecta estadísticas para simulaciones de recolección."""

    def __init__(self):
        self.datos = {
            "tiempos": [],
            "comida_recolectada": [],
            "agentes_activos": [],
            "conflictos": [],
        }

    def registrar_paso(self, entorno, agentes):
        """Registra datos del paso actual."""
        self.datos["tiempos"].append(entorno.tiempo)
        self.datos["comida_recolectada"].append(
            sum(getattr(a, "comida_recolectada", 0) for a in agentes)
        )
        self.datos["agentes_activos"].append(len(agentes))

        # Contar conflictos
        conflictos = 0
        for agente in agentes:
            conflictos += getattr(agente, "conflictos_ganados", 0)
            conflictos += getattr(agente, "conflictos_perdidos", 0)
        self.datos["conflictos"].append(conflictos)

    def mostrar_resumen(self, agentes):
        """Muestra resumen de estadísticas."""
        print("=== ESTADÍSTICAS FINALES ===")
        if self.datos["comida_recolectada"]:
            print(
                f"Total comida recolectada: {self.datos['comida_recolectada'][-1]}"
            )
        print(f"Agentes activos: {len(agentes)}")

        for agente in agentes:
            print(f"\nAgente {getattr(agente, 'id', 'N/A')}:")
            print(f"  Comida: {getattr(agente, 'comida_recolectada', 0)}")
            print(f"  Energía: {agente.energia}")

            if hasattr(agente, "conflictos_ganados"):
                print(f"  Conflictos ganados: {agente.conflictos_ganados}")
            if hasattr(agente, "conflictos_perdidos"):
                print(f"  Conflictos perdidos: {agente.conflictos_perdidos}")

    def graficar(self, titulo="Recolección de recursos"):
        if not self.datos["tiempos"]:
            print("No hay datos para graficar.")
            return

        tiempos = np.array(self.datos["tiempos"])
        comida = np.array(self.datos["comida_recolectada"])
        conflictos = np.array(self.datos["conflictos"])

        plt.figure()
        plt.plot(tiempos, comida, label="Comida total")
        plt.plot(tiempos, conflictos, linestyle="--", label="Conflictos acumulados")
        plt.xlabel("Paso de simulación")
        plt.ylabel("Valor")
        plt.title(titulo)
        plt.legend()
        plt.grid(True)
        plt.show()
