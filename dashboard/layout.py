import dash_bootstrap_components as dbc
from dash import html, dcc
from prediction_tab import prediction_tab
from heatmap_tab import heatmap_tab  # Add this import

layout = dbc.Container([ #layout for the dash app
    html.H2("Pakistan Wheat & Pesticide Dashboard", className="text-center my-4"),

    dcc.Tabs(id="tabs", value="dashboard-tab", children=[
        dcc.Tab(label="Dashboard", value="dashboard-tab"),
        dcc.Tab(label="Punjab Yield Map", value="map-tab"),
        dcc.Tab(label="Yield Heatmap", value="heatmap-tab"),  # Add this line
        dcc.Tab(label="Prediction", value="prediction-tab"),
    ]),

    html.Div(id="tab-content")  # placeholder for dynamic tab content
], fluid=True)