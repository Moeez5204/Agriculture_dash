from dash import html, dcc
import dash_bootstrap_components as dbc
from data_loader import load_pesticide_data, load_yield_data

#load data
pesticide_df = load_pesticide_data()
yield_df = load_yield_data()
unique_years = sorted(yield_df["Year"].dropna().unique())

#define layout
dashboard_tab = dbc.Container([
    dbc.Row([         # First column: dropdown to select between pesticide and yield view
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
        dbc.Col([         # Second column: dropdown to select year (only used when viewing yield)
            dcc.Dropdown(
                id="year-selector",
                options=[{"label": y, "value": y} for y in unique_years],
                value=unique_years[0],
                clearable=False
            )
        ], width=6)
    ]),
    html.Br(),#Line break for spacing
    dcc.Graph(id="graph-output")
])