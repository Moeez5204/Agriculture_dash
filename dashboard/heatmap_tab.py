
import plotly.express as px
from dash import html, dcc  # Added dcc to the import
import dash_bootstrap_components as dbc
from data_loader import load_yield_data, prepare_volatility_data

# Load and prepare data
yield_df = load_yield_data()
coord_df, vol_df = prepare_volatility_data()

# Clean and pivot data for heatmaps
def prepare_heatmap_data():
    # Yield heatmap (district × year)
    yield_heatmap = yield_df.pivot_table(
        index="District",
        columns="Year",
        values="Yield",
        aggfunc="mean"
    ).round(1)

    # Volatility heatmap (district × year)
    vol_heatmap = vol_df.pivot_table(
        index="District",
        columns="Year",
        values="Yield_StdDev",
        aggfunc="mean"
    ).round(2)

    # Normalize yield data
    yield_normalized = yield_heatmap.apply(
        lambda x: (x - x.mean()) / x.std(),
        axis=1
    )

    return {
        "yield_raw": yield_heatmap,
        "yield_normalized": yield_normalized,
        "volatility": vol_heatmap
    }

heatmap_data = prepare_heatmap_data()

# Dash layout
heatmap_tab = html.Div([
    html.H4("Punjab Wheat Yield Patterns", className="text-center mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Select(
                id="heatmap-metric",
                options=[
                    {"label": "Yield (Raw Values)", "value": "yield_raw"},
                    {"label": "Yield (Normalized by District)", "value": "yield_normalized"},
                    {"label": "Yield Volatility", "value": "volatility"}
                ],
                value="yield_raw",
            )
        ], width=6),

        dbc.Col([
            dbc.Select(
                id="color-scale",
                options=[
                    {"label": "Viridis", "value": "Viridis"},
                    {"label": "Plasma", "value": "Plasma"},
                    {"label": "RdYlGn", "value": "RdYlGn"},
                ],
                value="Viridis",
            )
        ], width=6)
    ], className="mb-4"),

    dbc.Card(dbc.CardBody(dcc.Graph(id="heatmap-graph", style={"height": "700px"}))),  # Fixed missing parenthesis

    html.Div(id="heatmap-summary", className="mt-4")
])
