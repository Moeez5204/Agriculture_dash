import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc
from data_loader import load_yield_data, prepare_volatility_data
from dash.dependencies import Input, Output

# Load and prepare data
yield_df = load_yield_data()
coord_df, vol_df = prepare_volatility_data()


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

    # Normalize yield data by district (z-score)
    yield_normalized = yield_heatmap.sub(yield_heatmap.mean(axis=1), axis=0).div(yield_heatmap.std(axis=1), axis=0)

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

    dbc.Card(dbc.CardBody(dcc.Graph(id="heatmap-graph", style={"height": "700px"}))),

    html.Div(id="heatmap-summary", className="mt-4")
])


# Add this callback to your callbacks.py file
def register_heatmap_callbacks(app):
    @app.callback(
        Output("heatmap-graph", "figure"),
        [Input("heatmap-metric", "value"),
         Input("color-scale", "value")]
    )
    def update_heatmap(metric, color_scale):
        data = heatmap_data[metric]

        fig = px.imshow(
            data,
            labels=dict(x="Year", y="District", color="Value"),
            x=data.columns,
            y=data.index,
            color_continuous_scale=color_scale,
            aspect="auto"
        )

        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="District",
            coloraxis_colorbar=dict(title="Value")
        )

        return fig