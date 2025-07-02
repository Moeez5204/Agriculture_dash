from dash import html, dcc
import dash_bootstrap_components as dbc
from data_loader import load_pesticide_data, load_yield_data

pesticide_df = load_pesticide_data()
yield_df = load_yield_data()
unique_years = sorted(yield_df["Year"].dropna().unique())

layout = dbc.Container([
    html.H2("Pakistan Wheat & Pesticide Dashboard", className="text-center my-4"),

    # Dropdowns
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="view-selector",
                options=[
                    {"label": "Pesticide Consumption", "value": "pesticide"},
                    {"label": "Wheat Yield by District", "value": "yield"},
                ],
                value="pesticide",
                clearable=False
            )
        ], width=6),
        dbc.Col([
            dcc.Dropdown(
                id="year-selector",
                options=[{"label": y, "value": y} for y in unique_years],
                value=unique_years[0],
                clearable=False,
                placeholder="Select Year for Yield",
            )
        ], width=6)
    ]),

    html.Br(),

    html.Div(id="graph-output")
], fluid=True)