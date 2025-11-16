"""Agente recolector con comunicación y aprendizaje (Ejercicios 4-6)."""

from typing import List, Dict, Set, Tuple, Optional, Any
import random
from collections import defaultdict, deque
from .agente_base import AgenteBase


class AgenteRecolector(AgenteBase):
    """
    Agente recolector que implementa:
    - Ejercicio 4: Comunicación entre agentes
    - Ejercicio 5: Memoria espacial (aprendizaje)
    - Ejercicio 6: Competencia por recursos
    """
    
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        modo: str = 'cooperativo',  # 'cooperativo' o 'competitivo'
        con_aprendizaje: bool = False
    ):
        """
        Inicializa el agente recolector.
        
        Args:
            x: Posición inicial en x
            y: Posición inicial en y
            modo: Modo de operación
            con_aprendizaje: Si debe aprender patrones espaciales
        """
        super().__init__(None, x, y)
        
        self.modo = modo
        self.con_aprendizaje = con_aprendizaje
        
        # Recursos recolectados
        self.comida_recolectada = 0
        self.energia = 100
        
        # Ejercicio 4: Sistema de comunicación
        self.mensajes_recibidos: List[Dict] = []
        self.objetivos_compartidos: Set[Tuple[int, int]] = set()
        self.objetivo_actual: Optional[Tuple[int, int]] = None
        
        # Ejercicio 5: Memoria espacial (mapa de calor)
        self.mapa_calor: Dict[Tuple[int, int], int] = defaultdict(int)
        self.posiciones_con_comida: Dict[Tuple[int, int], int] = defaultdict(int)
        
        # Ejercicio 6: Competencia
        self.agentes_cercanos: List[str] = []
        self.recursos_robados = 0
        self.bloqueos_sufridos = 0
        
        # Pathfinding
        self.plan: deque = deque()
    
    def percibir(self, entorno: Any) -> Dict:
        """
        Percibe el entorno de recolección.
        
        Returns:
            Dict con información del entorno
        """
        percepcion = {
            'hay_comida': entorno.hay_comida(self.x, self.y),
            'comida_visible': [],
            'agentes_visibles': [],
            'vecinos_validos': []
        }
        
        # Detectar comida en rango de visión (radio 5)
        radio = 5
        for dx in range(-radio, radio + 1):
            for dy in range(-radio, radio + 1):
                pos_x, pos_y = self.x + dx, self.y + dy
                if entorno.es_posicion_valida(pos_x, pos_y):
                    if entorno.hay_comida(pos_x, pos_y):
                        percepcion['comida_visible'].append((pos_x, pos_y))
        
        # Detectar otros agentes (Ejercicio 6: competencia)
        if hasattr(entorno, 'obtener_agentes_en'):
            agentes_cerca = entorno.obtener_agentes_en(self.x, self.y, radio=3)
            percepcion['agentes_visibles'] = [a.id for a in agentes_cerca if a.id != self.id]
            self.agentes_cercanos = percepcion['agentes_visibles']
        
        # Vecinos válidos
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = self.x + dx, self.y + dy
            if entorno.es_posicion_valida(nx, ny):
                percepcion['vecinos_validos'].append((nx, ny))
        
        return percepcion
    
    def decidir(self, percepcion: Dict) -> str:
        """
        Decide la acción basándose en percepción, comunicación y aprendizaje.
        
        Args:
            percepcion: Información del entorno
            
        Returns:
            Acción a ejecutar
        """
        # Si hay comida aquí, recolectar
        if percepcion['hay_comida']:
            return 'recolectar'
        
        # Si hay un plan activo, seguirlo
        if self.plan:
            return self.plan.popleft()
        
        # Ejercicio 4: Procesar mensajes de otros agentes
        self._procesar_mensajes()
        
        # Decidir objetivo
        objetivo = self._seleccionar_objetivo(percepcion)
        
        if objetivo:
            # Planificar ruta hacia objetivo
            camino = self._buscar_camino(objetivo, percepcion['vecinos_validos'])
            if camino:
                self.plan.extend(camino)
                return self.plan.popleft()
        
        # Ejercicio 5: Si tiene aprendizaje, ir a zonas con más comida
        if self.con_aprendizaje:
            mejor_zona = self._mejor_zona_aprendida()
            if mejor_zona:
                camino = self._buscar_camino(mejor_zona, percepcion['vecinos_validos'])
                if camino:
                    self.plan.extend(camino)
                    return self.plan.popleft()
        
        # Movimiento aleatorio
        if percepcion['vecinos_validos']:
            return self._direccion_hacia(random.choice(percepcion['vecinos_validos']))
        
        return 'esperar'
    
    def _seleccionar_objetivo(self, percepcion: Dict) -> Optional[Tuple[int, int]]:
        """
        Selecciona un objetivo considerando comunicación y competencia.
        
        Args:
            percepcion: Información del entorno
            
        Returns:
            Posición objetivo o None
        """
        comida_disponible = set(percepcion['comida_visible'])
        
        # Ejercicio 4: Filtrar objetivos ya reclamados por otros (cooperativo)
        if self.modo == 'cooperativo':
            comida_disponible -= self.objetivos_compartidos
        
        # Ejercicio 6: En modo competitivo, preferir comida cerca de otros agentes
        if self.modo == 'competitivo' and self.agentes_cercanos:
            # Ser más agresivo si hay competencia
            comida_lista = list(comida_disponible)
            if comida_lista:
                return min(comida_lista, key=lambda c: abs(c[0] - self.x) + abs(c[1] - self.y))
        
        # Seleccionar comida más cercana
        if comida_disponible:
            return min(
                comida_disponible,
                key=lambda c: abs(c[0] - self.x) + abs(c[1] - self.y)
            )
        
        return None
    
    def _buscar_camino(
        self,
        objetivo: Tuple[int, int],
        vecinos_validos: List[Tuple[int, int]]
    ) -> List[str]:
        """
        Búsqueda simple de camino (BFS simplificado).
        
        Args:
            objetivo: Posición objetivo
            vecinos_validos: Vecinos a considerar
            
        Returns:
            Lista de direcciones
        """
        # Movimiento simple hacia objetivo (greedy)
        dx = objetivo[0] - self.x
        dy = objetivo[1] - self.y
        
        movimientos = []
        
        if abs(dx) > abs(dy):
            if dx > 0:
                movimientos.append('derecha')
            else:
                movimientos.append('izquierda')
        else:
            if dy > 0:
                movimientos.append('abajo')
            else:
                movimientos.append('arriba')
        
        return movimientos[:3]  # Máximo 3 pasos
    
    def _direccion_hacia(self, posicion: Tuple[int, int]) -> str:
        """Calcula dirección hacia una posición."""
        dx = posicion[0] - self.x
        dy = posicion[1] - self.y
        
        if abs(dx) > abs(dy):
            return 'derecha' if dx > 0 else 'izquierda'
        else:
            return 'abajo' if dy > 0 else 'arriba'
    
    def actuar(self, accion: str, entorno: Any) -> None:
        """
        Ejecuta la acción en el entorno.
        
        Args:
            accion: Acción a ejecutar
            entorno: Entorno de recolección
        """
        if accion == 'recolectar':
            # Recolectar comida
            if entorno.recolectar_comida(self.x, self.y):
                self.comida_recolectada += 1
                self.energia += 20
                
                # Ejercicio 5: Registrar éxito en mapa de calor
                if self.con_aprendizaje:
                    self.posiciones_con_comida[(self.x, self.y)] += 1
                    self._actualizar_mapa_calor(self.x, self.y, recompensa=10)
                
                # Limpiar objetivo actual
                self.objetivo_actual = None
        
        elif accion in ['arriba', 'abajo', 'izquierda', 'derecha']:
            # Mover
            dx, dy = {
                'arriba': (0, -1),
                'abajo': (0, 1),
                'izquierda': (-1, 0),
                'derecha': (1, 0)
            }[accion]
            
            nuevo_x, nuevo_y = self.x + dx, self.y + dy
            
            if entorno.es_posicion_valida(nuevo_x, nuevo_y):
                self.x, self.y = nuevo_x, nuevo_y
                self.energia -= 1
                
                # Ejercicio 5: Actualizar mapa de calor
                if self.con_aprendizaje:
                    self._actualizar_mapa_calor(self.x, self.y, recompensa=1)
    
    # Ejercicio 4: Comunicación
    def enviar_mensaje(self, otros_agentes: List['AgenteRecolector'], tipo: str, contenido: Any):
        """
        Envía mensaje a otros agentes.
        
        Args:
            otros_agentes: Lista de agentes receptores
            tipo: Tipo de mensaje
            contenido: Contenido del mensaje
        """
        for agente in otros_agentes:
            if agente.id != self.id:
                agente.recibir_mensaje(self.id, tipo, contenido)
    
    def recibir_mensaje(self, remitente: str, tipo: str, contenido: Any):
        """
        Recibe mensaje de otro agente.
        
        Args:
            remitente: ID del agente remitente
            tipo: Tipo de mensaje
            contenido: Contenido del mensaje
        """
        self.mensajes_recibidos.append({
            'de': remitente,
            'tipo': tipo,
            'contenido': contenido
        })
    
    def _procesar_mensajes(self):
        """Procesa mensajes recibidos."""
        for mensaje in self.mensajes_recibidos:
            if mensaje['tipo'] == 'objetivo_reclamado':
                # Otro agente va por este objetivo
                self.objetivos_compartidos.add(mensaje['contenido'])
        
        self.mensajes_recibidos.clear()
    
    # Ejercicio 5: Aprendizaje espacial
    def _actualizar_mapa_calor(self, x: int, y: int, recompensa: int):
        """
        Actualiza el mapa de calor con la recompensa.
        
        Args:
            x: Posición x
            y: Posición y
            recompensa: Valor de recompensa
        """
        self.mapa_calor[(x, y)] += recompensa
        
        # Propagar a vecinos (decaimiento)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            self.mapa_calor[(x + dx, y + dy)] += recompensa // 2
    
    def _mejor_zona_aprendida(self) -> Optional[Tuple[int, int]]:
        """
        Retorna la mejor zona según el aprendizaje.
        
        Returns:
            Posición de mejor zona o None
        """
        if not self.mapa_calor:
            return None
        
        return max(self.mapa_calor.items(), key=lambda x: x[1])[0]
    
    def get_estadisticas(self) -> Dict:
        """Retorna estadísticas del agente."""
        return {
            'id': self.id,
            'posicion': (self.x, self.y),
            'comida_recolectada': self.comida_recolectada,
            'energia': self.energia,
            'modo': self.modo,
            'zonas_aprendidas': len(self.mapa_calor),
            'objetivos_compartidos': len(self.objetivos_compartidos),
            'agentes_cercanos': len(self.agentes_cercanos)
        }
