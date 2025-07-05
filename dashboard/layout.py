import dash_bootstrap_components as dbc
from dash import html, dcc


#layout

layout = dbc.Container([
    html.H2("Pakistan Wheat & Pesticide Dashboard", className="text-center my-4"),

    dcc.Tabs(id="tabs", value="dashboard-tab", children=[
        dcc.Tab(label="Dashboard", value="dashboard-tab"),
        dcc.Tab(label="Punjab Yield Map", value="map-tab")
    ]),

    html.Div(id="tab-content")  # placeholder for dynamic tab content
], fluid=True)