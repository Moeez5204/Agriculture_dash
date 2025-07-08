import dash_bootstrap_components as dbc
from dash import html, dcc
from prediciton_tab import *
#layout

layout = dbc.Container([
    html.H2("Pakistan Wheat & Pesticide Dashboard", className="text-center my-4"),

    dcc.Tabs(id="tabs", value="dashboard-tab", children=[
        dcc.Tab(label="Dashboard", value="dashboard-tab"),
        dcc.Tab(label="Punjab Yield Map", value="map-tab"),
        dcc.Tab(label='Prediction', children=[prediction_tab])  # 👈 Add this line

    ]),

    html.Div(id="tab-content")  # placeholder for dynamic tab content
], fluid=True)