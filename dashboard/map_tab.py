# This file creates a Dash tab that displays a map of Punjab with red markers for each district.

# Import necessary libraries
import pandas as pd
from dash import html, dcc
import plotly.express as px
from data_loader import load_yield_data, compute_yield_volatility

#Load long-format yield data
yield_df = load_yield_data()

#Compute volatility
vol_df = compute_yield_volatility(yield_df)

# Add categorical volatility level based on percentiles
low_thres = vol_df["Yield_StdDev"].quantile(1/3)
high_thres = vol_df["Yield_StdDev"].quantile(2/3)

def categorize_volatility(stddev):
    if stddev <= low_thres:
        return "Low"
    elif stddev <= high_thres:
        return "Medium"
    else:
        return "High"

vol_df["Volatility_Level"] = vol_df["Yield_StdDev"].apply(categorize_volatility)

# 3. Merge with coordinates
coord_df = pd.read_csv("data/Punjab_District_Coord.csv")
coord_df = coord_df.merge(vol_df, on="District", how="left")

# 4. Create a mapbox scatter plot with district markers
fig = px.scatter_mapbox(
    coord_df,
    lat="Latitude",
    lon="Longitude",
    hover_name="District",
    hover_data={"Yield_StdDev": True, "Volatility_Level": True},  # Include volatility and level in hover
    zoom=6.5,
    height=600
)

# Customize hover tooltip to show district name, volatility, and level
fig.update_traces(
    hovertemplate="District: %{hovertext}<br>Volatility: %{customdata[0]:.2f}T/Ha<br>Level: %{customdata[1]}<extra></extra>"
)

# Set map style and remove layout margins and legend
fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    showlegend=False
)

# Set red color and size for district markers
fig.update_traces(marker=dict(size=10, color="red"))

# Create Dash layout container for the map tab
map_tab = html.Div([
    html.H4("Punjab Wheat Yield Map"),
    dcc.Graph(figure=fig)
])