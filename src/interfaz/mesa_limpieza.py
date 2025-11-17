# src/interfaz/mesa_limpieza.py
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

import random


class LimpiezaAgent(Agent):
    """Agente de limpieza simple para Mesa."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.suciedad_limpiada = 0
        self.lugares_visitados = set()

    def step(self):
        x, y = self.pos
        self.lugares_visitados.add((x, y))

        # Limpiar si hay suciedad
        if (x, y) in self.model.suciedad:
            self.model.suciedad.remove((x, y))
            self.suciedad_limpiada += 1
            return

        # Mover a una celda vecina no visitada si es posible
        vecinos = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        random.shuffle(vecinos)

        for nx, ny in vecinos:
            if (nx, ny) not in self.lugares_visitados:
                self.model.grid.move_agent(self, (nx, ny))
                return

        # Si todas vecinas están visitadas, se queda quieto


class LimpiezaModel(Model):
    """Modelo ABM de limpieza con Mesa."""

    def __init__(self, width=10, height=10, num_agentes=1, num_suciedad=20):
        super().__init__()
        self.width = width
        self.height = height
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, torus=False)
        self.running = True

        # Generar suciedad
        self.suciedad = set()
        for _ in range(num_suciedad):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.suciedad.add((x, y))

        # Crear agentes
        for i in range(num_agentes):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            agente = LimpiezaAgent(i, self)
            self.grid.place_agent(agente, (x, y))
            self.schedule.add(agente)

    def step(self):
        self.schedule.step()
        if not self.suciedad:
            self.running = False


# ==== Visualización Mesa ====

def limpieza_portrayal(agent):
    if agent is None:
        return

    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.5,
        "Layer": 1,
        "Color": "red",
    }
    return portrayal


def suciedad_portrayal(x, y, model):
    """Factory para dibujar suciedad como objetos de fondo."""
    if (x, y) in model.suciedad:
        return {
            "Shape": "rect",
            "Filled":
