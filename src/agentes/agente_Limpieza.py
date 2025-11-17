# src/agentes/agente_limpieza.py
import random
from typing import Set, Dict, Tuple, Any, Optional, List

from .agente_base import AgenteBase


class AgenteLimpiezaBase(AgenteBase):
    """Agente limpiador básico."""

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.suciedad_limpiada = 0
        self.historial_movimientos: List[Dict[str, Any]] = []

    def registrar_paso(self, accion: str):
        self.historial_movimientos.append(
            {
                "x": self.x,
                "y": self.y,
                "accion": accion,
                "energia": self.energia,
            }
        )

    def percibir(self, entorno) -> bool:
        """Percibe si hay suciedad en su celda actual."""
        return entorno.hay_suciedad(self.x, self.y)

    def decidir(self, percepcion: bool) -> str:
        """Si hay suciedad, limpia; si no, se mueve aleatoriamente."""
        if percepcion:
            return "limpiar"
        return random.choice(["arriba", "abajo", "izquierda", "derecha"])

    def actuar(self, decision: str, entorno) -> None:
        if decision == "limpiar":
            if entorno.limpiar(self.x, self.y):
                self.suciedad_limpiada += 1
        elif decision in ["arriba", "abajo", "izquierda", "derecha"]:
            self.mover(decision, entorno)

        self.registrar_paso(decision)


class AgenteLimpiezaConMemoria(AgenteLimpiezaBase):
    """Ejercicio 1: Agente que recuerda lugares visitados y NO repite celdas."""

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.lugares_visitados: Set[Tuple[int, int]] = set()
        self.ultima_direccion: Optional[str] = None

    def decidir(self, percepcion: bool) -> str:
        # Registrar posición actual
        self.lugares_visitados.add((self.x, self.y))

        if percepcion:
            return "limpiar"

        # Priorizar direcciones hacia celdas NO visitadas
        direcciones_no_visitadas = []
        for dx, dy, direccion in [
            (0, -1, "arriba"),
            (0, 1, "abajo"),
            (-1, 0, "izquierda"),
            (1, 0, "derecha"),
        ]:
            nx, ny = self.x + dx, self.y + dy
            if (nx, ny) not in self.lugares_visitados:
                direcciones_no_visitadas.append(direccion)

        if direcciones_no_visitadas:
            self.ultima_direccion = random.choice(direcciones_no_visitadas)
            return self.ultima_direccion

        # Si TODO alrededor ya fue visitado, se queda en espera (no repite)
        return "esperar"

    def actuar(self, decision: str, entorno) -> None:
        if decision == "limpiar":
            if entorno.limpiar(self.x, self.y):
                self.suciedad_limpiada += 1
        elif decision == "esperar":
            # No se mueve ni gasta energía
            pass
        else:
            self.mover(decision, entorno)

        self.registrar_paso(decision)


class AgenteLimpiezaConTipos(AgenteLimpiezaBase):
    """Ejercicio 2: Agente que maneja diferentes tipos de suciedad."""

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.tipos_limpiados: Dict[str, int] = {}
        self.puntos_totales = 0

    def decidir(self, percepcion: Any) -> str:
        if percepcion:
            return "limpiar"
        return random.choice(["arriba", "abajo", "izquierda", "derecha"])

    def actuar(self, decision: str, entorno) -> None:
        if decision == "limpiar":
            resultado: Optional[Tuple[str, int]] = entorno.limpiar(self.x, self.y)
            if resultado:
                tipo, puntos = resultado
                self.suciedad_limpiada += 1
                self.tipos_limpiados[tipo] = self.tipos_limpiados.get(tipo, 0) + 1
                self.puntos_totales += puntos
        else:
            self.mover(decision, entorno)

        self.registrar_paso(decision)


class AgenteLimpiezaConEvasion(AgenteLimpiezaBase):
    """
    Ejercicio 3: Agente que evita obstáculos.
    Proceso: DETECTAR -> EVITAR -> REPLANIFICAR.
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.obstaculos_detectados: Set[Tuple[int, int]] = set()
        self.ultimo_scan: List[Dict[str, Any]] = []

    def escanear_obstaculos(self, entorno):
        """Escanea un radio de 1 casilla alrededor y guarda reporte detallado."""
        self.ultimo_scan.clear()
        etiquetas = {
            (-1, -1): "arriba-izquierda",
            (0, -1): "arriba",
            (1, -1): "arriba-derecha",
            (-1, 0): "izquierda",
            (1, 0): "derecha",
            (-1, 1): "abajo-izquierda",
            (0, 1): "abajo",
            (1, 1): "abajo-derecha",
        }

        for (dx, dy), nombre in etiquetas.items():
            nx, ny = self.x + dx, self.y + dy
            if entorno.es_valida(nx, ny):
                hay_obs = entorno.hay_obstaculo(nx, ny)
                if hay_obs:
                    self.obstaculos_detectados.add((nx, ny))
                self.ultimo_scan.append(
                    {
                        "direccion": nombre,
                        "pos": (nx, ny),
                        "obstaculo": hay_obs,
                    }
                )

    def percibir(self, entorno) -> bool:
        """Detecta suciedad y escanea obstáculos cercanos."""
        self.escanear_obstaculos(entorno)
        return super().percibir(entorno)

    def decidir(self, percepcion: bool) -> str:
        if percepcion:
            return "limpiar"

        # EVITAR: filtrar direcciones seguras
        direcciones_seguras = []
        for dx, dy, direccion in [
            (0, -1, "arriba"),
            (0, 1, "abajo"),
            (-1, 0, "izquierda"),
            (1, 0, "derecha"),
        ]:
            nx, ny = self.x + dx, self.y + dy
            if (nx, ny) not in self.obstaculos_detectados:
                direcciones_seguras.append(direccion)

        if direcciones_seguras:
            # REPLANIFICAR: elegir entre las seguras
            return random.choice(direcciones_seguras)

        # Si todo alrededor está marcado como peligroso, no moverse
        return "esperar"

    def actuar(self, decision: str, entorno) -> None:
        if decision == "limpiar":
            if entorno.limpiar(self.x, self.y):
                self.suciedad_limpiada += 1
        elif decision == "esperar":
            pass
        else:
            self.mover(decision, entorno)

        self.registrar_paso(decision)
