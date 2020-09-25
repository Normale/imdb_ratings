import plotly
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
from imdb_api import get_series_data
import pandas as pd


BACKGROUND = "white"
COLORS = px.colors.diverging.RdYlGn
COLORS.insert(0, BACKGROUND)
# COLORS = ['rgb(165,0,38)', 'rgb(215,48,39)', 'rgb(244,109,67)', 'rgb(253,174,97)', 'rgb(254,224,139)', 'rgb(255,255,191)', 'rgb(217,239,139)', 'rgb(166,217,106)', 'rgb(102,189,99)', 'rgb(26,152,80)', 'rgb(0,104,55)']
# Aggresive colors:
# COLORS = [BACKGROUND] + ['rgb(165,0,38)'] + 3 * ['rgb(215,48,39)'] + ['rgb(244,109,67)',
                                                                    #   'rgb(253,174,97)', 'rgb(254,224,139)', 'rgb(102,189,99)', 'rgb(26,152,80)', 'rgb(0,104,55)']
LINE_COLORS = [BACKGROUND] + 10 * ["rgb(200,212,227)"]


key = "fd10716c"  # omdb key

def create_heatmap(question, hm_click):
    d = get_series_data(question, key)
    values = pd.DataFrame([[float(episode['imdbRating']) for episode in season if (
        episode != None and episode['imdbRating'] != "N/A")] for season in d]).fillna(0).transpose()[::-1]
    nr_seasons = len(values.columns)
    # nr_episodes = len(max(d, key=len))
    nr_episodes = len(values)   


    x_axis = list(range(1, nr_seasons + 1))
    y_axis = list(range(1, nr_episodes + 1))
    y_axis = y_axis[::-1]
    hover = []

    for i in range(nr_episodes):
        row = []
        for j in range(nr_seasons):
            try:
                row.append(
                    f"<b>{d[j][i]['Title']}</b><br>Season: {j+1} Episode: {i+1}</br><br>{d[j][i]['Released']} </br>")
            except IndexError:
                row.append("")
        hover.append(row)
    # invert lists
    hover = hover[::-1]
    # Make Annotated Heatmap
    annotations = []
    for episode_nr in values.values:
        x_list = []
        for element in episode_nr:
            if element == 0:
                element = ""
            x_list.append(element)
        annotations.append(x_list)

    fig = ff.create_annotated_heatmap(
        values.values, annotation_text=annotations,
                        text=hover,
                        x=x_axis, y=y_axis,
                        colorscale=COLORS, 
                        font_colors=['black'],
                        hoverinfo='text',
                        zmin = 1.0,
                        zmax = 10.0
                        
    )

    fig.update_layout(title_text=f'{question} IMDB RATINGS',
                    height = 400  + nr_episodes * 25,
                    width = 200 + nr_seasons * 40,
                    yaxis = {
                           "autorange": "reversed",
                           "fixedrange": True
                           },
                    xaxis = { "fixedrange": True }
                    )

    return fig
if __name__ == "__main__":
    question = "Friends"
    fig = create_heatmap(question, None)
    fig.show()
