# src/interfaz/ui_mesa_ej4.py
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

import random


class RecolectorMesa(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.comida = 0

    def step(self):
        # Movimiento aleatorio simple (demo)
        posibles = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=False
        )
        nueva_pos = self.random.choice(posibles)
        self.model.grid.move_agent(self, nueva_pos)

        # Comer si hay recurso
        if nueva_pos in self.model.recursos:
            self.model.recursos.remove(nueva_pos)
            self.comida += 1


class ModeloRecoleccionMesa(Model):
    def __init__(self, width=10, height=10, num_agents=3, num_recursos=15):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.recursos = set()

        # Crear recursos
        for _ in range(num_recursos):
            x = random.randrange(width)
            y = random.randrange(height)
            self.recursos.add((x, y))

        # Crear agentes
        for i in range(num_agents):
            a = RecolectorMesa(i, self)
            self.schedule.add(a)
            x = random.randrange(width)
            y = random.randrange(height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        self.schedule.step()


def recursos_portrayal(model):
    portrayals = []

    # Agentes
    for (contents, x, y) in model.grid.coord_iter():
        for agent in contents:
            portrayals.append(
                {
                    "Shape": "circle",
                    "Filled": "true",
                    "r": 0.8,
                    "Layer": 1,
                    "x": x,
                    "y": y,
                    "Color": "red",
                    "text": str(agent.comida),
                    "text_color": "white",
                }
            )

    # Recursos
    for (x, y) in model.recursos:
        portrayals.append(
            {
                "Shape": "rect",
                "Filled": "true",
                "w": 0.7,
                "h": 0.7,
                "Layer": 0,
                "x": x,
                "y": y,
                "Color": "green",
            }
        )

    return portrayals


def lanzar_servidor():
    grid = CanvasGrid(recursos_portrayal, 10, 10, 500, 500)
    server = ModularServer(
        ModeloRecoleccionMesa,
        [grid],
        "Recolectores (demo Mesa)",
        {"width": 10, "height": 10, "num_agents": 4, "num_recursos": 20},
    )
    server.port = 8521
    server.launch()


if __name__ == "__main__":
    lanzar_servidor()
