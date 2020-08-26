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
from heatmap import create_heatmap

from imdb_api import get_series_data

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport",
                "content": "width=device-width, initial-scale=1"}],
)

server = app.server
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
                value="chernobyl"
            ),
            html.Br(),
            html.Div(
                id="reset-btn-outer",
                children=html.Button(id="reset-btn", children="Reset", n_clicks=0),
            ),
        ],
    )


# def generate_patient_volume_heatmap(title, hm_click, reset):
#     """
#     :param: hm_click: clickData from heatmap.
#     :param: reset (boolean): reset heatmap graph if True.

#     :return: Patient volume annotated heatmap.
#     """
#     if title is None: title = "Breaking Bad"
#     episodes_data = get_series_data(title)
#     print(episodes_data)
#     nr_seasons = len(episodes_data)
#     nr_episodes = len(max(episodes_data, key=len))
#     print(nr_episodes, nr_seasons)
#     x_axis = [x+1 for x in range(nr_seasons)]
#     # y_axis = [-(x+1) for x in range(nr_episodes)]
#     # y_axis = y_axis[::-1]

#     # hour_of_day = ""
#     # weekday = ""
#     # shapes = []
#     # hover = []
#     # for i in range(nr_episodes):
#     #     row = []
#     #     for j in range(nr_seasons):
#     #         try:
#     #             row.append(
#     #                 f"<br>{episodes_data[j][i]['Title']}</br>\
#     #                 <br>{episodes_data[j][i]['Released']}</br>")
#     #         except IndexError:
#     #             row.append("")
#     #     hover.append(row)
#     # # invert lists
#     # hover = hover[::-1]

#     if hm_click is not None:
#         hour_of_day = hm_click["points"][0]["x"]
#         weekday = hm_click["points"][0]["y"]

#         # Add shapes
#         x0 = x_axis.index(hour_of_day) / 24
#         x1 = x0 + 1 / 24
#         y0 = y_axis.index(weekday) / 7
#         y1 = y0 + 1 / 7

#         shapes = [
#             dict(
#                 type="rect",
#                 xref="paper",
#                 yref="paper",
#                 x0=x0,
#                 x1=x1,
#                 y0=y0,
#                 y1=y1,
#                 line=dict(color="#ff6347"),
#             )
        # ]
    # z = pd.DataFrame([[float(episode['imdbRating']) for episode in season if (
    # episode != None and episode['imdbRating'] != "N/A")] for season in episodes_data]).fillna(0).transpose()[::-1]

    
    # Heatmap

    # data = [
    #     dict(
    #         # x=x_axis,
    #         # y=y_axis,
    #         # z=z.values,
    #         type="heatmap",
    #         name="",
    #         # text=hover,
    #         hoverinfo='text',
    #         showscale=True,
    #         colorscale=COLORS,
    #         reversed = True
    #     )
    # ]

    # return {"data": data}

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
                # Patient Volume Heatmap
                html.Div(
                    id="imdb_ratings_card",
                    children=[
                        html.B(""),
                        html.Hr(),
                        dcc.Graph(id="patient_volume_hm"),
                    ]
                )
        ],
                ),
            ],
        )


@app.callback(
    Output("patient_volume_hm", "figure"),
[
        Input("title-input", "value"),
        Input("patient_volume_hm", "clickData"),
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
    app.run_server(debug = True)
