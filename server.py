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


canvas_element = CanvasGrid(sickle_cell_portrayal, 100, 100, 700, 700)
chart_element = ChartModule(
    [{"Label": "Normal Adults", "Color": "#16981C"}, {"Label": "Carrier Adults", "Color": "#FFFD0F"},
     {"Label": "Sickle Cell Adults", "Color": "FF130F"}, {"Label": "Normal Children", "Color": "0FFFDE"},
     {"Label": "Carrier Children", "Color": "FFD80F"}, {"Label": "Sickle Cell Children", "Color": "FF0FB0"}]
)

model_params = {
    "initial_normal_adult": UserSettableParameter(
        "slider", "Normal Adults", value=500, min_value=100, max_value=800, step=5
    ),
    "initial_carrier_adult": UserSettableParameter(
        "slider", "Carrier Adults", value=500, min_value=100, max_value=800, step=5
    ),
    "initial_sickle_adult": UserSettableParameter(
        "slider", "Afflicted Adults", value=500, min_value=100, max_value=800, step=5
    ),
    "malaria_prevalence": UserSettableParameter(
        "slider", "Prevalence of Malaria", value=0.5, min_value=0, max_value=1, step=0.01
    ),
    "sickle_cell_deadliness": UserSettableParameter(
        "slider", "Sickle Cell Deadliness", value=0.5, min_value=0, max_value=1, step=0.01
    ),
    "heterozygous_advantage": UserSettableParameter(
        "slider", "Heterozygous Advantage", value=0.5, min_value=0, max_value=1, step=0.01
    )

}

server = ModularServer(
    SickleSim, [canvas_element, chart_element], "Sickle Cell Selection", model_params
)
server.port = 8521