import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

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