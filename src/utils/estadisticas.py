# src/utils/estadisticas.py
from typing import Dict, Any, List
import time


class EstadisticasLimpieza:
    """Recolecta estadísticas para simulaciones de limpieza."""

    def __init__(self):
        self.datos: Dict[str, List[Any]] = {
            "tiempos": [],
            "suciedad_limpiada": [],
            "lugares_visitados": [],
            "eficiencia": [],
        }
        self.inicio_tiempo = None

    def iniciar(self):
        self.inicio_tiempo = time.time()

    def registrar_paso(self, entorno, agente):
        t = time.time() - self.inicio_tiempo if self.inicio_tiempo else 0
        self.datos["tiempos"].append(t)
        self.datos["suciedad_limpiada"].append(
            getattr(agente, "suciedad_limpiada", 0)
        )
        self.datos["lugares_visitados"].append(
            len(getattr(agente, "lugares_visitados", set()))
        )

        total_celdas = entorno.ancho * entorno.alto
        if hasattr(agente, "lugares_visitados") and total_celdas > 0:
            eff = len(agente.lugares_visitados) / total_celdas * 100
            self.datos["eficiencia"].append(eff)

    def mostrar_resumen(self, agente):
        print("=== ESTADÍSTICAS FINALES (LIMPIEZA) ===")
        print(f"Suciedad limpiada: {getattr(agente, 'suciedad_limpiada', 0)}")
        print(f"Lugares visitados: {len(getattr(agente, 'lugares_visitados', set()))}")
        if hasattr(agente, "puntos_totales"):
            print(f"Puntos totales: {agente.puntos_totales}")
        if hasattr(agente, "tipos_limpiados"):
            print(f"Tipos limpiados: {agente.tipos_limpiados}")
        if self.datos["eficiencia"]:
            print(f"Eficiencia: {self.datos['eficiencia'][-1]:.1f}%")


class EstadisticasRecoleccion:
    """Recolecta estadísticas para simulaciones de recolección."""

    def __init__(self):
        self.datos: Dict[str, List[Any]] = {
            "tiempos": [],
            "comida_recolectada": [],
            "agentes_activos": [],
            "conflictos": [],
        }

    def registrar_paso(self, entorno, agentes):
        self.datos["tiempos"].append(entorno.tiempo)
        self.datos["comida_recolectada"].append(
            sum(getattr(a, "comida_recolectada", 0) for a in agentes)
        )
        self.datos["agentes_activos"].append(len(agentes))

        conflictos = 0
        for a in agentes:
            conflictos += getattr(a, "conflictos_ganados", 0)
            conflictos += getattr(a, "conflictos_perdidos", 0)
        self.datos["conflictos"].append(conflictos)

    def mostrar_resumen(self, agentes):
        print("=== ESTADÍSTICAS FINALES (RECOLECCIÓN) ===")
        if self.datos["comida_recolectada"]:
            print(
                f"Total comida recolectada: {self.datos['comida_recolectada'][-1]}"
            )
        print(f"Agentes activos: {len(agentes)}")
        for a in agentes:
            print(f"\nAgente {getattr(a, 'id', 'N/A')}:")
            print(f"  Comida: {getattr(a, 'comida_recolectada', 0)}")
            print(f"  Energía: {a.energia}")
            if hasattr(a, "conflictos_ganados"):
                print(f"  Conflictos ganados: {a.conflictos_ganados}")
            if hasattr(a, "conflictos_perdidos"):
                print(f"  Conflictos perdidos: {a.conflictos_perdidos}")
