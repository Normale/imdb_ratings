import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction
import plotly.figure_factory as ff

import numpy as np
import pandas as pd
import datetime
from datetime import datetime as dt
import pathlib
import flask

from heatmap import create_heatmap

from imdb_api import get_series_data

server = flask.Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    meta_tags=[{"name": "viewport",
                "content": "width=device-width, initial-scale=1"}],
)

app.config.suppress_callback_exceptions = True

BACKGROUND = "black"
COLORS = [BACKGROUND] +['rgb(165,0,38)'] + 3 * ['rgb(215,48,39)'] + ['rgb(244,109,67)', 'rgb(253,174,97)','rgb(254,224,139)', 'rgb(102,189,99)', 'rgb(26,152,80)', 'rgb(0,104,55)']
KEY = "fd10716c"


def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.P("Put Title in"),
            dcc.Input(
                id="title-input",
                value="",
                placeholder="e.g. Breaking Bad",
                debounce=True
            ),
            html.Br(),
            html.Div(
                id="reset-btn-outer",
                children=html.Button(id="reset-btn", children="Reset", n_clicks=0),
            ),
        ],
    )


app.layout = html.Div(
    id="app-container",
    children=[
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[generate_control_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                # Series Volume Heatmap
                html.Div(
                    id="imdb_ratings_card",
                    children=[
                        html.B(""),
                        html.Hr(),
                        dcc.Graph(id="series_hm"),
                    ]
                )
        ],
                ),
            ],
        )


@app.callback(
    Output("series_hm", "figure"),
[
        Input("title-input", "value"),
        Input("series_hm", "clickData"),
    ],
)
def update_heatmap(title, hm_click):
    reset = False
    # Find which one has been triggered
    ctx=dash.callback_context
    
    if ctx.triggered:
        prop_id=ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "reset-btn":
            reset=True

    # Return to original hm(no colored annotation) by resetting
    # return generate_patient_volume_heatmap(title, hm_click, reset)
    return create_heatmap(title, hm_click)
'''
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("wait_time_table", "children")] + wait_time_inputs + score_inputs,
)'''

# Run the server
if __name__ == "__main__":
    app.server.run(debug=True)
