from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from agents import AdultSickle, AdultNormal, AdultCarrier, ChildSickle, ChildCarrier, ChildNormal
from model import SickleSim


def sickle_cell_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is AdultNormal:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.3
        portrayal["Color"] = "#00FF53"

    elif type(agent) is AdultCarrier:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.3
        portrayal["Color"] = "#F5e70F"

    elif type(agent) is AdultSickle:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.3
        portrayal["Color"] = "#F50F23"

    elif type(agent) is ChildNormal:
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.3
        portrayal["h"] = 0.3
        portrayal["Color"] = "#F50F23"

    elif type(agent) is ChildCarrier:
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.3
        portrayal["h"] = 0.3
        portrayal["Color"] = "#F50F23"

    elif type(agent) is ChildSickle:
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.3
        portrayal["h"] = 0.3
        portrayal["Color"] = "#F50F23"

    return portrayal


canvas_element = CanvasGrid(sickle_cell_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
)

model_params = {
    "grass": UserSettableParameter("checkbox", "Grass Enabled", True),
    "grass_regrowth_time": UserSettableParameter(
        "slider", "Grass Regrowth Time", 20, 1, 50
    ),
    "initial_sheep": UserSettableParameter(
        "slider", "Initial Sheep Population", 100, 10, 300
    ),
    "sheep_reproduce": UserSettableParameter(
        "slider", "Sheep Reproduction Rate", 0.04, 0.01, 1.0, 0.01
    ),
    "initial_wolves": UserSettableParameter(
        "slider", "Initial Wolf Population", 50, 10, 300
    ),
    "wolf_reproduce": UserSettableParameter(
        "slider",
        "Wolf Reproduction Rate",
        0.05,
        0.01,
        1.0,
        0.01,
        description="The rate at which wolf agents reproduce.",
    ),
    "wolf_gain_from_food": UserSettableParameter(
        "slider", "Wolf Gain From Food Rate", 20, 1, 50
    ),
    "sheep_gain_from_food": UserSettableParameter(
        "slider", "Sheep Gain From Food", 4, 1, 10
    ),
}

server = ModularServer(
    SickleSim, [canvas_element, chart_element], "Sickle Cell Selection", model_params
)
server.port = 8521