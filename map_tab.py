import pandas as pd
from dash import html, dcc
import plotly.express as px

#map tab


coord_df = pd.read_csv("Punjab_District_Coord.csv")

fig = px.scatter_mapbox(
    coord_df,
    lat="Latitude",
    lon="Longitude",
    hover_name="District",
    zoom=6.5,
    height=600
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0, "t":0, "l":0, "b":0},
    showlegend=False
)
fig.update_traces(marker=dict(size=10, color="red"))

map_tab = html.Div([
    html.H4("Punjab Wheat Yield Map"),
    dcc.Graph(figure=fig)
])