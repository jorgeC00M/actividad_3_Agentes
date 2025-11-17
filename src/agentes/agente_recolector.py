# src/agentes/agente_recolector.py
import random
import json
import os
from typing import List, Dict, Any, Set, Tuple, Optional
from collections import deque

from .agente_base import AgenteBase


class AgenteRecolectorBase(AgenteBase):
    """Agente recolector básico con planificación de ruta (BFS)."""

    def __init__(self, x: int, y: int, agent_id: Optional[str] = None):
        super().__init__(x, y, agent_id)
        self.comida_recolectada = 0
        self.plan: List[str] = []
        self._entorno = None
        self.objetivo_actual: Optional[Tuple[int, int]] = None

    def percibir(self, entorno):
        """Percibe comida en un radio de 5 y almacena referencia al entorno."""
        self._entorno = entorno
        return entorno.obtener_comida_cercana(self.x, self.y, radio=5)

    def planificar_ruta(self, objetivo: Optional[Tuple[int, int]]) -> List[str]:
        """Planifica ruta con BFS evitando obstáculos."""
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
        """Escoge comida más cercana o se mueve aleatoriamente."""
        if not self.plan:
            if percepcion:
                objetivo = min(
                    percepcion, key=lambda c: abs(c[0] - self.x) + abs(c[1] - self.y)
                )
                self.objetivo_actual = objetivo
                self.plan = self.planificar_ruta(objetivo)

            if self.plan:
                return self.plan.pop(0)

            self.objetivo_actual = None
            return random.choice(["arriba", "abajo", "izquierda", "derecha"])

        return self.plan.pop(0)

    def actuar(self, decision: str, entorno) -> None:
        if decision in ["arriba", "abajo", "izquierda", "derecha"]:
            self.mover(decision, entorno)
            # recolectar si pisa comida
            if entorno.hay_comida(self.x, self.y):
                if entorno.recolectar_comida(self.x, self.y):
                    self.comida_recolectada += 1
                    self.energia += 10
                    self.plan = []
                    self.objetivo_actual = None


class AgenteRecolectorComunicativo(AgenteRecolectorBase):
    """Ejercicio 4: Recolector que se comunica con otros para evitar conflictos."""

    def __init__(self, x: int, y: int, agent_id: Optional[str] = None):
        super().__init__(x, y, agent_id)
        self.mensajes: List[Dict[str, Any]] = []
        self.objetivos_reservados: Set[Tuple[int, int]] = set()
        self.mensajes_enviados: int = 0

    def enviar_mensaje(self, otros_agentes, tipo: str, contenido: Any) -> None:
        """Envía mensajes a otros agentes (se contabilizan para eficiencia)."""
        self.mensajes_enviados += len(otros_agentes)
        for agente in otros_agentes:
            if hasattr(agente, "recibir_mensaje"):
                agente.recibir_mensaje(self.id, tipo, contenido)

    def recibir_mensaje(self, remitente: str, tipo: str, contenido: Any) -> None:
        self.mensajes.append({"de": remitente, "tipo": tipo, "contenido": contenido})

    def procesar_mensajes(self) -> List[Tuple[int, int]]:
        """Procesa mensajes pendientes: comida compartida y objetivos reservados."""
        comida_reportada: List[Tuple[int, int]] = []
        for msg in self.mensajes:
            if msg["tipo"] == "comida_encontrada":
                comida_reportada.append(msg["contenido"])
            elif msg["tipo"] == "objetivo_reservado":
                self.objetivos_reservados.add(msg["contenido"])
        self.mensajes.clear()
        return comida_reportada

    def decidir(self, percepcion) -> str:
        # Primero procesar mensajes recibidos
        comida_compartida = self.procesar_mensajes()

        if not self.plan:
            # Combinar comida vista + compartida
            todas_opciones = list(set(percepcion + comida_compartida))
            # Filtrar posiciones ya reservadas
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
                # Reservar objetivo para evitar que otros vayan
                self.objetivos_reservados.add(objetivo)

            if self.plan:
                return self.plan.pop(0)

            self.objetivo_actual = None
            return random.choice(["arriba", "abajo", "izquierda", "derecha"])

        return self.plan.pop(0)


class AgenteRecolectorConAprendizaje(AgenteRecolectorBase):
    """
    Ejercicio 5:
    Agente que aprende qué ÁREAS tienen más comida (memoria espacial).
    - Mantiene memoria por celda: memoria_comida[(x,y)] = veces que encontró comida.
    - Agrupa por áreas 2x2 → areas_productivas.
    - Guarda areas_productivas en JSON para usar en futuras ejecuciones.
    """

    def __init__(self, x: int, y: int, agent_id: Optional[str] = None):
        super().__init__(x, y, agent_id)
        self.memoria_comida: Dict[Tuple[int, int], int] = {}
        self.areas_productivas: Set[Tuple[int, int]] = set()
        # archivo de memoria persistente
        self._ruta_memoria = "mem_ej5_areas.json"
        self.cargar_memoria_areas()

    # --- Persistencia entre ejecuciones ---

    def cargar_memoria_areas(self):
        if os.path.exists(self._ruta_memoria):
            try:
                with open(self._ruta_memoria, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.areas_productivas = set(tuple(a) for a in data.get("areas", []))
            except Exception:
                self.areas_productivas = set()

    def guardar_memoria_areas(self):
        try:
            data = {"areas": [list(a) for a in self.areas_productivas]}
            with open(self._ruta_memoria, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception:
            pass

    # --- Lógica de aprendizaje ---

    def actualizar_memoria(self, posicion: Tuple[int, int], encontro_comida: bool) -> None:
        if posicion not in self.memoria_comida:
            self.memoria_comida[posicion] = 0
        if encontro_comida:
            self.memoria_comida[posicion] += 1

        if self.energia % 10 == 0:
            self.identificar_areas_productivas()

    def identificar_areas_productivas(self) -> None:
        """
        Agrupa la memoria en áreas de 2x2.
        Si la frecuencia media de un área > 0.3 → se considera productiva.
        """
        areas: Dict[Tuple[int, int], List[int]] = {}
        for (x, y), freq in self.memoria_comida.items():
            area = (x // 2, y // 2)  # area_x, area_y
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
                # Si no se ve comida, ir a una de las áreas productivas conocidas
                area_obj = random.choice(list(self.areas_productivas))
                cx = area_obj[0] * 2 + 1
                cy = area_obj[1] * 2 + 1
                opciones_priorizadas = [(cx, cy)]

            if opciones_priorizadas:
                objetivo = min(
                    opciones_priorizadas,
                    key=lambda c: abs(c[0] - self.x) + abs(c[1] - self.y),
                )
                self.objetivo_actual = objetivo
                self.plan = self.planificar_ruta(objetivo)

            if self.plan:
                return self.plan.pop(0)

            self.objetivo_actual = None
            return random.choice(["arriba", "abajo", "izquierda", "derecha"])

        return self.plan.pop(0)


class AgenteCompetitivo(AgenteRecolectorComunicativo):
    """
    Ejercicio 6:
    Agente competitivo por recursos limitados.
    Estrategias:
    - agresiva: casi siempre compite
    - conservadora: compite si hay pocos rivales
    - evasiva: evita competir cuando hay rivales cerca
    """

    def __init__(
        self, x: int, y: int, agent_id: Optional[str] = None, estrategia: str = "agresiva"
    ):
        super().__init__(x, y, agent_id)
        self.estrategia = estrategia
        self.conflictos_ganados = 0
        self.conflictos_perdidos = 0
        self.rivales_actuales: List[AgenteBase] = []

    def percibir(self, entorno):
        percepcion_comida = super().percibir(entorno)
        # detectar rivales cercanos (radio 2)
        self.rivales_actuales = []
        for agente in entorno.agentes:
            if agente is not self:
                distancia = abs(agente.x - self.x) + abs(agente.y - self.y)
                if distancia <= 2:
                    self.rivales_actuales.append(agente)
        return percepcion_comida

    def detectar_rivales_cercanos(self) -> List[AgenteBase]:
        return self.rivales_actuales

    def evaluar_competencia(self, objetivo: Optional[Tuple[int, int]]) -> bool:
        rivales = self.detectar_rivales_cercanos()
        if objetivo is None:
            return True

        if self.estrategia == "agresiva":
            return True
        if self.estrategia == "conservadora":
            return len(rivales) <= 1
        # evasiva
        return len(rivales) == 0

    def decidir(self, percepcion) -> str:
        decision = super().decidir(percepcion)

        # Evaluar si mantiene el objetivo o se retira (conflicto perdido)
        if self.objetivo_actual is not None and self.plan:
            quiere = self.evaluar_competencia(self.objetivo_actual)
            if not quiere:
                # se retira del conflicto
                self.conflictos_perdidos += 1
                self.plan = []
                self.objetivo_actual = None
                return random.choice(["arriba", "abajo", "izquierda", "derecha"])
            else:
                if self.rivales_actuales:
                    self.conflictos_ganados += 1

        return decision
