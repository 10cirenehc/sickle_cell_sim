import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import datetime as dt
app = dash.Dash(__name__)

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "CoSim"


# these are the controls where the parameters can be tuned.
# They are not placed on the screen here, we just define them.
# Each separate input (e.g. a slider for the fatality rate) is placed
# in its own "dbc.FormGroup" and gets a "dbc.Label" where we put its name.
# The sliders use the predefined "dcc.Slider"-class, the numeric inputs
# use "dbc.Input", etc., so we don't have to tweak anything ourselves.
# The controls are wrappen in a "dbc.Card" so they look nice.
controls = dbc.Card(
    [

        dbc.FormGroup(
            [
                dbc.Label("Initial number of normal people"),
                dbc.Input(
                    id="initial_cases", type="number", placeholder="initial_cases",
                    min=1, max=400_000, step=1, value=10,
                )
            ]
        ),

        dbc.FormGroup(
            [
                dbc.Label("Initial number of Homozygotes"),
                dbc.Input(
                    id="population", type="number", placeholder="population",
                    min=10_000, max=400_000, step=10_000, value=80_000_000,
                )
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label('Initial number of Heterozygotes'),
                dbc.Input(
                    id="icu_beds", type="number", placeholder="ICU Beds per 100k",
                    min=0.0, max=400_000, step=0.1, value=34.0,
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label('Probability of going to ICU when infected (%)'),
                html.Br(),
                dcc.Slider(
                    id='p_I_to_C',
                    min=0.01,
                    max=100.0,
                    step=0.01,
                    value=5.0,
                    tooltip={'always_visible': True, "placement": "bottom"}
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label('Probability of dying in ICU (%)'),
                dcc.Slider(
                    id='p_C_to_D',
                    min=0.01,
                    max=100.0,
                    step=0.01,
                    value=50.0,
                    tooltip={'always_visible': True, "placement": "bottom"}
                ),
            ]
        ),
        # this is the input where the R value can be changed over time.
        # It is implemented as a table where the date is in the first column,
        # and users can change the R value on that date in the second column.
        dbc.FormGroup(
            [
                dbc.Label('Reproduction rate R over time'),
                dash_table.DataTable(
                    id='r0_table',
                    columns=[
                        {"name": "Date", "id": "Date"},
                        {"name": "R value", "id": "R value",
                         "editable": True, "type": "numeric"},
                    ],
                    data=[
                        {
                            "Date": i[0],
                            "R value": i[1],
                        }
                        for i in [("2020-01-01", 3.2), ("2020-02-01", 2.9), ("2020-03-01", 2.5), ("2020-04-01", 0.8), ("2020-05-01", 1.1), ("2020-06-01", 2.0), ("2020-07-01", 2.1), ("2020-08-01", 2.2), ("2020-09-01", 2.3)]
                    ],
                    style_cell_conditional=[
                        {'if': {'column_id': 'Date'},
                         'width': '5px'},
                        {'if': {'column_id': 'R value'},
                         'width': '10px'},
                    ],
                    style_cell={'textAlign': 'left',
                                'fontSize': 16, 'font-family': 'Helvetica'},
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    },

                ),
            ]
        ),
        dbc.Button("Apply", id="submit-button-state",
                   color="primary", block=True)
    ],
    body=True,
)
# the layout; that's everything you can see in the dashboard
app.layout = html.Div(children=[
    html.H1(children='Hello World!'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Montreal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

# this makes the dashboard run when you type "python3 app.py" in your terminal
if __name__ == '__main__':
    app.run_server(debug=True)