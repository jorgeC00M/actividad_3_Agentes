# src/agentes/agente_limpieza.py
import random
from typing import Set, Dict, Tuple, Any, Optional, List

from .agente_base import AgenteBase


class AgenteLimpiezaBase(AgenteBase):
    """Agente limpiador básico."""

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.suciedad_limpiada = 0
        # Para mostrar el camino / pasos en interfaz o consola
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
        """Percibe si hay suciedad en la celda actual."""
        return entorno.hay_suciedad(self.x, self.y)

    def decidir(self, percepcion: bool) -> str:
        """Decisión básica: limpiar si hay suciedad, sino moverse al azar."""
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
    """
    Ejercicio 1:
    Agente que recuerda lugares visitados y trata de NO ir 2 veces a la misma celda.
    Si todas las celdas vecinas ya fueron visitadas → se queda en 'esperar'.
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.lugares_visitados: Set[Tuple[int, int]] = set()
        self.ultima_direccion: Optional[str] = None

    def decidir(self, percepcion: bool) -> str:
        # Registrar la celda actual como visitada
        self.lugares_visitados.add((self.x, self.y))

        if percepcion:
            # Primero limpiar si hay suciedad
            return "limpiar"

        # Buscar direcciones hacia celdas NO visitadas
        direcciones_no_visitadas = []
        for dx, dy, direccion in [
            (0, -1, "arriba"),
            (0, 1, "abajo"),
            (-1, 0, "izquierda"),
            (1, 0, "derecha"),
        ]:
            nx, ny = self.x + dx, self.y + dy
            # No filtramos por entorno.es_valida aquí: mover() ya valida bordes
            if (nx, ny) not in self.lugares_visitados:
                direcciones_no_visitadas.append(direccion)

        if direcciones_no_visitadas:
            self.ultima_direccion = random.choice(direcciones_no_visitadas)
            return self.ultima_direccion

        # Todas las vecinas ya visitadas → no moverse para no repetir
        return "esperar"

    def actuar(self, decision: str, entorno) -> None:
        if decision == "limpiar":
            if entorno.limpiar(self.x, self.y):
                self.suciedad_limpiada += 1
        elif decision == "esperar":
            # No gastar energía, solo registrar paso
            pass
        else:
            self.mover(decision, entorno)

        self.registrar_paso(decision)


class AgenteLimpiezaConTipos(AgenteLimpiezaBase):
    """
    Ejercicio 2:
    Agente que maneja tipos de suciedad con distintos valores (puntaje).
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.tipos_limpiados: Dict[str, int] = {}
        self.puntos_totales: int = 0

    def decidir(self, percepcion: bool) -> str:
        if percepcion:
            return "limpiar"
        return random.choice(["arriba", "abajo", "izquierda", "derecha"])

    def actuar(self, decision: str, entorno) -> None:
        if decision == "limpiar":
            resultado = entorno.limpiar(self.x, self.y)
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
    Ejercicio 3:
    Agente que DETECTA → EVITA → REPLANIFICA frente a obstáculos.

    - Escanea en un radio de 1 (3x3 alrededor) con nombres:
      arriba-izquierda, arriba, arriba-derecha, etc.
    - Además guarda obstáculos en un radio de 2 en obstaculos_detectados.
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.obstaculos_detectados: Set[Tuple[int, int]] = set()
        self.ultimo_scan: List[Dict[str, Any]] = []

    def escanear_obstaculos(self, entorno):
        """Escanea alrededor y guarda información textual para la interfaz/consola."""
        self.ultimo_scan.clear()

        # 1) Scan fino en radio 1 para la descripción tipo:
        # Arriba-izquierda, Arriba, ...
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

        # 2) Scan más amplio (radio 2) para acumular memoria de obstáculos
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                nx, ny = self.x + dx, self.y + dy
                if entorno.es_valida(nx, ny) and entorno.hay_obstaculo(nx, ny):
                    self.obstaculos_detectados.add((nx, ny))

    def percibir(self, entorno) -> bool:
        self.escanear_obstaculos(entorno)
        return super().percibir(entorno)

    def decidir(self, percepcion: bool) -> str:
        if percepcion:
            return "limpiar"

        # REPLANIFICAR → buscar direcciones seguras sin obstáculos detectados
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
            return random.choice(direcciones_seguras)

        # Rodeado de obstáculos → mejor esperar
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
