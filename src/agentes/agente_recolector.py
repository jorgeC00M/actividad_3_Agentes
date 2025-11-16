"""
Agentes recolectores - Ejercicios 4, 5 y 6
"""

import random
from typing import List, Dict, Any, Set
from collections import deque
from .agente_base import AgenteBase


class AgenteRecolectorBase(AgenteBase):
    """Agente recolector básico (código original mejorado)"""
    
    def __init__(self, x: int, y: int, agent_id: str = None):
        super().__init__(x, y, agent_id)
        self.comida_recolectada = 0
        self.plan: List[str] = []
        self._entorno = None  # Referencia al entorno para planificar_ruta
    
    def percibir(self, entorno):
        return entorno.obtener_comida_cercana(self.x, self.y, radio=5)
    
    def planificar_ruta(self, objetivo, entorno):
        """BFS para encontrar camino al objetivo"""
        if objetivo is None:
            return []
            
        cola = deque([(self.x, self.y, [])])
        visitados = {(self.x, self.y)}
        
        while cola:
            x, y, camino = cola.popleft()
            
            if (x, y) == objetivo:
                return camino
                
            for dx, dy, direccion in [(0, -1, 'arriba'), (0, 1, 'abajo'),
                                    (-1, 0, 'izquierda'), (1, 0, 'derecha')]:
                nx, ny = x + dx, y + dy
                if (entorno.es_valida(nx, ny) and 
                    (nx, ny) not in visitados and 
                    not entorno.hay_obstaculo(nx, ny)):
                    visitados.add((nx, ny))
                    cola.append((nx, ny, camino + [direccion]))
        
        return []
    
    def decidir(self, percepcion):
        if not self.plan:
            if percepcion:
                # Elegir comida más cercana
                objetivo = min(percepcion, 
                             key=lambda c: abs(c[0] - self.x) + abs(c[1] - self.y))
                self.plan = self.planificar_ruta(objetivo, self._entorno)
            
            if self.plan:
                return self.plan.pop(0)
            else:
                return random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
        else:
            return self.plan.pop(0)
    
    def actuar(self, decision, entorno):
        self._entorno = entorno  # Guardar referencia para planificar_ruta
        
        if decision in ['arriba', 'abajo', 'izquierda', 'derecha']:
            self.mover(decision, entorno)
            
            # Recolectar comida si está en esta posición
            if entorno.hay_comida(self.x, self.y):
                if entorno.recolectar_comida(self.x, self.y):
                    self.comida_recolectada += 1
                    self.energia += 10
                    self.plan = []  # Limpiar plan actual


class AgenteRecolectorComunicativo(AgenteRecolectorBase):
    """Ejercicio 4: Agente que se comunica con otros para evitar conflictos"""
    
    def __init__(self, x: int, y: int, agent_id: str = None):
        super().__init__(x, y, agent_id)
        self.mensajes: List[Dict] = []
        self.objetivos_reservados: Set[tuple] = set()
    
    def enviar_mensaje(self, otros_agentes, tipo: str, contenido: Any):
        for agente in otros_agentes:
            if hasattr(agente, 'recibir_mensaje'):
                agente.recibir_mensaje(self.id, tipo, contenido)
    
    def recibir_mensaje(self, remitente: str, tipo: str, contenido: Any):
        self.mensajes.append({
            'de': remitente,
            'tipo': tipo,
            'contenido': contenido
        })
    
    def procesar_mensajes(self):
        comida_reportada = []
        for msg in self.mensajes:
            if msg['tipo'] == 'comida_encontrada':
                comida_reportada.append(msg['contenido'])
            elif msg['tipo'] == 'objetivo_reservado':
                self.objetivos_reservados.add(msg['contenido'])
        self.mensajes.clear()
        return comida_reportada
    
    def decidir(self, percepcion):
        # Procesar mensajes antes de decidir
        comida_compartida = self.procesar_mensajes()
        
        if not self.plan:
            # Combinar percepciones locales y compartidas
            todas_opciones = list(set(percepcion + comida_compartida))
            # Filtrar objetivos ya reservados
            opciones_disponibles = [obj for obj in todas_opciones 
                                  if obj not in self.objetivos_reservados]
            
            if opciones_disponibles:
                objetivo = min(opciones_disponibles,
                             key=lambda c: abs(c[0] - self.x) + abs(c[1] - self.y))
                self.plan = self.planificar_ruta(objetivo, self._entorno)
                # Reservar objetivo
                self.objetivos_reservados.add(objetivo)
            
            if self.plan:
                return self.plan.pop(0)
            else:
                return random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
        else:
            return self.plan.pop(0)


class AgenteRecolectorConAprendizaje(AgenteRecolectorBase):
    """Ejercicio 5: Agente que aprende áreas con más comida"""
    
    def __init__(self, x: int, y: int, agent_id: str = None):
        super().__init__(x, y, agent_id)
        self.memoria_comida: Dict[tuple, int] = {}  # (x,y): frecuencia
        self.areas_productivas: Set[tuple] = set()  # (area_x, area_y)
    
    def actualizar_memoria(self, posicion: tuple, encontro_comida: bool):
        if posicion not in self.memoria_comida:
            self.memoria_comida[posicion] = 0
        
        if encontro_comida:
            self.memoria_comida[posicion] += 1
        
        # Actualizar áreas productivas periódicamente
        if self.energia % 10 == 0:
            self.identificar_areas_productivas()
    
    def identificar_areas_productivas(self):
        # Agrupar por áreas de 2x2
        areas = {}
        for (x, y), freq in self.memoria_comida.items():
            area = (x // 2, y // 2)
            if area not in areas:
                areas[area] = []
            areas[area].append(freq)
        
        # Identificar áreas con alta frecuencia
        self.areas_productivas.clear()
        for area, frecuencias in areas.items():
            if frecuencias and sum(frecuencias) / len(frecuencias) > 0.3:
                self.areas_productivas.add(area)
    
    def decidir(self, percepcion):
        # Actualizar memoria
        self.actualizar_memoria((self.x, self.y), self._entorno.hay_comida(self.x, self.y))
        
        if not self.plan:
            opciones_priorizadas = []
            
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
                objetivo = min(opciones_priorizadas,
                             key=lambda c: abs(c[0] - self.x) + abs(c[1] - self.y))
                self.plan = self.planificar_ruta(objetivo, self._entorno)
            
            if self.plan:
                return self.plan.pop(0)
            else:
                return random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
        else:
            return self.plan.pop(0)


class AgenteCompetitivo(AgenteRecolectorComunicativo):
    """Ejercicio 6: Agente competitivo por recursos limitados"""
    
    def __init__(self, x: int, y: int, agent_id: str = None, estrategia: str = 'agresiva'):
        super().__init__(x, y, agent_id)
        self.estrategia = estrategia
        self.conflictos_ganados = 0
        self.conflictos_perdidos = 0
    
    def detectar_rivales_cercanos(self, otros_agentes, radio: int = 2):
        rivales = []
        for agente in otros_agentes:
            if agente.id != self.id:
                distancia = abs(agente.x - self.x) + abs(agente.y - self.y)
                if distancia <= radio:
                    rivales.append(agente)
        return rivales
    
    def evaluar_competencia(self, objetivo, otros_agentes):
        rivales = self.detectar_rivales_cercanos(otros_agentes)
        
        if self.estrategia == 'agresiva':
            return True  # Siempre competir
        elif self.estrategia == 'conservadora':
            return len(rivales) <= 1  # Competir solo si hay pocos rivales
        else:  # 'evasiva'
            return len(rivales) == 0  # Competir solo si no hay rivales
    
    def decidir(self, percepcion):
        # Lógica de decisión con evaluación competitiva
        return super().decidir(percepcion)