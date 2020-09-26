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

    #optional space for creating e.g. RESET button


    return create_heatmap(title, hm_click)

# Run the server
if __name__ == "__main__":
    app.server.run(debug=True)
