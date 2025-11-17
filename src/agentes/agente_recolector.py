# src/agentes/agente_recolector.py
import os
import random
from typing import List, Dict, Any, Set, Tuple, Optional
from collections import deque

import numpy as np

from .agente_base import AgenteBase


class AgenteRecolectorBase(AgenteBase):
    """Agente recolector básico con planificación de ruta (BFS)."""

    def __init__(self, x: int, y: int, agent_id: Optional[str] = None):
        super().__init__(x, y, agent_id)
        self.comida_recolectada = 0
        self.plan: List[str] = []
        self._entorno = None  # Referencia al entorno para planificar_ruta
        self.objetivo_actual: Optional[Tuple[int, int]] = None

    def percibir(self, entorno):
        """Guarda el entorno y percibe comida cercana."""
        self._entorno = entorno
        return entorno.obtener_comida_cercana(self.x, self.y, radio=5)

    def planificar_ruta(self, objetivo: Optional[Tuple[int, int]]) -> List[str]:
        """BFS para encontrar camino al objetivo usando self._entorno."""
        entorno = self._entorno
        if objetivo is None or entorno is None:
            return []

        cola = deque([(self.x, self.y, [])])
        visitados = {(self.x, self.y)}

        while cola:
            x, y, camino = cola.popleft()

            if (x, y) == objetivo:
                return camino

            for dx, dy, direccion in [
                (0, -1, "arriba"),
                (0, 1, "abajo"),
                (-1, 0, "izquierda"),
                (1, 0, "derecha"),
            ]:
                nx, ny = x + dx, y + dy
                if (
                    entorno.es_valida(nx, ny)
                    and (nx, ny) not in visitados
                    and not entorno.hay_obstaculo(nx, ny)
                ):
                    visitados.add((nx, ny))
                    cola.append((nx, ny, camino + [direccion]))

        return []

    def decidir(self, percepcion) -> str:
        """
        Si no tiene plan:
         - elige la comida más cercana y planifica ruta
         - si no hay comida visible, se mueve aleatoriamente.
        """
        if not self.plan:
            if percepcion:
                objetivo = min(
                    percepcion, key=lambda c: abs(c[0] - self.x) + abs(c[1] - self.y)
                )
                self.objetivo_actual = objetivo
                self.plan = self.planificar_ruta(objetivo)

            if self.plan:
                return self.plan.pop(0)

            # Sin plan ni comida visible: moverse al azar
            self.objetivo_actual = None
            return random.choice(["arriba", "abajo", "izquierda", "derecha"])

        # Si ya tenía un plan, seguirlo
        return self.plan.pop(0)

    def actuar(self, decision: str, entorno) -> None:
        if decision in ["arriba", "abajo", "izquierda", "derecha"]:
            self.mover(decision, entorno)

            # Recolectar comida si está en esta posición
            if entorno.hay_comida(self.x, self.y):
                if entorno.recolectar_comida(self.x, self.y):
                    self.comida_recolectada += 1
                    self.energia += 10
                    # Al alcanzar comida, limpiamos el plan y el objetivo
                    self.plan = []
                    self.objetivo_actual = None


class AgenteRecolectorComunicativo(AgenteRecolectorBase):
    """Ejercicio 4: Agente que se comunica con otros para evitar conflictos."""

    def __init__(self, x: int, y: int, agent_id: Optional[str] = None):
        super().__init__(x, y, agent_id)
        self.mensajes: List[Dict[str, Any]] = []
        self.objetivos_reservados: Set[Tuple[int, int]] = set()
        self.mensajes_enviados: int = 0

    def enviar_mensaje(self, otros_agentes, tipo: str, contenido: Any) -> None:
        self.mensajes_enviados += len(otros_agentes)
        for agente in otros_agentes:
            if hasattr(agente, "recibir_mensaje"):
                agente.recibir_mensaje(self.id, tipo, contenido)

    def recibir_mensaje(self, remitente: str, tipo: str, contenido: Any) -> None:
        self.mensajes.append({"de": remitente, "tipo": tipo, "contenido": contenido})

    def procesar_mensajes(self) -> List[Tuple[int, int]]:
        comida_reportada: List[Tuple[int, int]] = []
        for msg in self.mensajes:
            if msg["tipo"] == "comida_encontrada":
                comida_reportada.append(msg["contenido"])
            elif msg["tipo"] == "objetivo_reservado":
                self.objetivos_reservados.add(msg["contenido"])
        self.mensajes.clear()
        return comida_reportada

    def decidir(self, percepcion) -> str:
        # Procesar mensajes antes de decidir
        comida_compartida = self.procesar_mensajes()

        if not self.plan:
            # Combinar percepciones locales y compartidas
            todas_opciones = list(set(percepcion + comida_compartida))

            # Filtrar objetivos ya reservados
            opciones_disponibles = [
                obj for obj in todas_opciones if obj not in self.objetivos_reservados
            ]

            if opciones_disponibles:
                objetivo = min(
                    opciones_disponibles,
                    key=lambda c: abs(c[0] - self.x) + abs(c[1] - self.y),
                )
                self.objetivo_actual = objetivo
                self.plan = self.planificar_ruta(objetivo)
                # Reservar objetivo
                self.objetivos_reservados.add(objetivo)

            if self.plan:
                return self.plan.pop(0)

            # Sin plan: movimiento aleatorio
            self.objetivo_actual = None
            return random.choice(["arriba", "abajo", "izquierda", "derecha"])

        # Ya tiene plan: seguirlo
        return self.plan.pop(0)


class AgenteRecolectorConAprendizaje(AgenteRecolectorBase):
    """Ejercicio 5: Agente que aprende áreas con más comida y recuerda entre ejecuciones."""

    def __init__(self, x: int, y: int, agent_id: Optional[str] = None):
        super().__init__(x, y, agent_id)
        self.memoria_comida: Dict[Tuple[int, int], int] = {}  # (x,y): frecuencia
        self.areas_productivas: Set[Tuple[int, int]] = set()  # (area_x, area_y)
        # Persistencia de áreas productivas entre ejecuciones
        self._ruta_memoria = "mem_ej5_areas.npy"
        self.cargar_memoria_areas()

    def cargar_memoria_areas(self):
        if os.path.exists(self._ruta_memoria):
            data = np.load(self._ruta_memoria, allow_pickle=True).item()
            self.areas_productivas = set(data.get("areas", []))

    def guardar_memoria_areas(self):
        data = {"areas": list(self.areas_productivas)}
        np.save(self._ruta_memoria, data)

    def actualizar_memoria(self, posicion: Tuple[int, int], encontro_comida: bool) -> None:
        if posicion not in self.memoria_comida:
            self.memoria_comida[posicion] = 0

        if encontro_comida:
            self.memoria_comida[posicion] += 1

        # Actualizar áreas productivas periódicamente
        if self.energia % 10 == 0:
            self.identificar_areas_productivas()

    def identificar_areas_productivas(self) -> None:
        """Agrupa celdas en áreas 2x2 y marca las de mayor frecuencia media."""
        areas: Dict[Tuple[int, int], List[int]] = {}
        for (x, y), freq in self.memoria_comida.items():
            area = (x // 2, y // 2)
            areas.setdefault(area, []).append(freq)

        self.areas_productivas.clear()
        for area, frecuencias in areas.items():
            if frecuencias and sum(frecuencias) / len(frecuencias) > 0.3:
                self.areas_productivas.add(area)

    def decidir(self, percepcion) -> str:
        # Actualizar memoria con la celda actual
        if self._entorno is not None:
            self.actualizar_memoria(
                (self.x, self.y), self._entorno.hay_comida(self.x, self.y)
            )

        if not self.plan:
            opciones_priorizadas: List[Tuple[int, int]] = []

            if percepcion:
                # Priorizar comida en áreas productivas
                for comida in percepcion:
                    area_comida = (comida[0] // 2, comida[1] // 2)
                    if area_comida in self.areas_productivas:
                        opciones_priorizadas.insert(0, comida)
                    else:
                        opciones_priorizadas.append(comida)
            elif self.areas_productivas:
                # Ir a áreas productivas si no hay comida visible
                area_objetivo = random.choice(list(self.areas_productivas))
                centro_x = area_objetivo[0] * 2 + 1
                centro_y = area_objetivo[1] * 2 + 1
                opciones_priorizadas = [(centro_x, centro_y)]

            if opciones_priorizadas:
                objetivo = min(
                    opciones_priorizadas,
                    key=lambda c: abs(c[0] - self.x) + abs(c[1] - self.y),
                )
                self.objetivo_actual = objetivo
                self.plan = self.planificar_ruta(objetivo)

            if self.plan:
                return self.plan.pop(0)

            # Sin plan ni áreas productivas: movimiento aleatorio
            self.objetivo_actual = None
            return random.choice(["arriba", "abajo", "izquierda", "derecha"])

        return self.plan.pop(0)


class AgenteCompetitivo(AgenteRecolectorComunicativo):
    """Ejercicio 6: Agente competitivo por recursos limitados."""

    def __init__(
        self,
        x: int,
        y: int,
        agent_id: Optional[str] = None,
        estrategia: str = "agresiva",
    ):
        super().__init__(x, y, agent_id)
        self.estrategia = estrategia  # 'agresiva', 'conservadora', 'evasiva'
        self.conflictos_ganados = 0
        self.conflictos_perdidos = 0
        self.rivales_actuales: List[AgenteBase] = []

    def percibir(self, entorno):
        """Percibe comida y rivales cercanos."""
        percepcion_comida = super().percibir(entorno)

        # Detectar rivales cercanos (radio 2)
        self.rivales_actuales = []
        for agente in entorno.agentes:
            if agente is not self:
                distancia = abs(agente.x - self.x) + abs(agente.y - self.y)
                if distancia <= 2:
                    self.rivales_actuales.append(agente)

        return percepcion_comida

    def detectar_rivales_cercanos(self) -> List[AgenteBase]:
        """Devuelve la lista de rivales detectados en la última percepción."""
        return self.rivales_actuales

    def evaluar_competencia(
        self, objetivo: Optional[Tuple[int, int]]
    ) -> bool:
        """
        Devuelve True si el agente decide competir por el objetivo,
        según su estrategia y los rivales cercanos.
        """
        rivales = self.detectar_rivales_cercanos()

        if objetivo is None:
            return True

        if self.estrategia == "agresiva":
            return True  # Siempre competir
        if self.estrategia == "conservadora":
            return len(rivales) <= 1  # Competir solo si hay pocos rivales
        # 'evasiva'
        return len(rivales) == 0  # Solo si no hay rivales

    def decidir(self, percepcion) -> str:
        """
        Usa la lógica comunicativa base, pero puede abandonar el objetivo
        si la evaluación competitiva lo desaconseja.
        """
        decision = super().decidir(percepcion)

        if self.objetivo_actual is not None and self.plan:
            quiere_competir = self.evaluar_competencia(self.objetivo_actual)

            if not quiere_competir:
                # Renuncia al objetivo: lo contamos como conflicto perdido potencial
                self.conflictos_perdidos += 1
                self.plan = []
                self.objetivo_actual = None
                return random.choice(["arriba", "abajo", "izquierda", "derecha"])
            else:
                if self.rivales_actuales:
                    self.conflictos_ganados += 1

        return decision
