# This file creates a Dash tab that displays a map of Punjab with red markers for each district.

# Import necessary libraries
import pandas as pd
from dash import html, dcc
import plotly.express as px

# Load district coordinates from CSV
coord_df = pd.read_csv("Punjab_District_Coord.csv") #Read Csv Data

# Create a mapbox scatter plot with district markers
fig = px.scatter_mapbox( #Places graph ontop of map to show cities
    coord_df,
    lat="Latitude",
    lon="Longitude",
    hover_name="District",
    hover_data={},
    zoom=6.5,
    height=600
)
# Customize hover tooltip to only show district name
fig.update_traces(hovertemplate="%{hovertext}<extra></extra>") #Removes lat and long on hover

# Set map style and remove layout margins and legend
fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0, "t":0, "l":0, "b":0},
    showlegend=False
) # places map of Punjab
# Set red color and size for district markers
fig.update_traces(marker=dict(size=10, color="red"))

# Create Dash layout container for the map tab
map_tab = html.Div([
    html.H4("Punjab Wheat Yield Map"),
    dcc.Graph(figure=fig)
])