import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from imdb_api import get_series_data
import pandas as pd

BACKGROUND = "black"
# COLORS = px.colors.diverging.RdYlGn
# COLORS[0] = "rgb(0,0,0)"#"rgb(255,255,255)" #white for empty cells, to make then invisible
#['rgb(165,0,38)', 'rgb(215,48,39)', 'rgb(244,109,67)', 'rgb(253,174,97)', 'rgb(254,224,139)', 'rgb(255,255,191)', 'rgb(217,239,139)', 'rgb(166,217,106)', 'rgb(102,189,99)', 'rgb(26,152,80)', 'rgb(0,104,55)']
#Aggresive colors:
COLORS = [BACKGROUND] +['rgb(165,0,38)'] + 3 * ['rgb(215,48,39)'] + ['rgb(244,109,67)', 'rgb(253,174,97)','rgb(254,224,139)', 'rgb(102,189,99)', 'rgb(26,152,80)', 'rgb(0,104,55)']
LINE_COLORS = [BACKGROUND] + 10 * ["rgb(200,212,227)"]

key = "fd10716c" #omdb key
question = "Friends"
d = get_series_data(question, key)

max_length = len(max(d,key=len))

df = pd.DataFrame(d)

values = pd.DataFrame([[float(episode['imdbRating']) for episode in season if (episode != None and episode['imdbRating']!="N/A")] for season in d]).fillna(0)
# values is 2D array of seasons[episodesRating]
# values = [[1.1,2,3.3,4], [1,2,3.5,4,5]] 

fig = go.Figure( data=[go.Table(

                        columnwidth=[50,100],
                        header=dict(
                           values=[''] + [x+1 for x in range(len(df))],
                           line = dict(color="rgb(200,212,227)", width=[0.4]),
                           fill_color = "black",
                           font_color = "white"
                           )  ,
                        cells=dict(
                           values=[[x+1 for x in range(max_length)]] + [[value for value in season if value != 0] for season in values.values],
                           fill_color= [["black"]] + [np.array(COLORS)[np.array(season).astype(int)] for season in values.values],
                           line=dict(
                              color = "black",
                              # color=[["rgb(200,212,227)"]] + [np.array(LINE_COLORS)[np.array(season).astype(int)] for season in values.values],
                              width=[0.4, 0.6]),
                           align='center',
                           font=dict(color=["white", "black"], size=11),
                        )
                        )
                     ])
fig.show()
