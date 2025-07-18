import pandas as pd
from dash import Input, Output, html
from dashboard_tab import dashboard_tab
from map_tab import map_tab
from heatmap_tab import heatmap_tab, register_heatmap_callbacks  # Added heatmap_tab import
from data_loader import load_pesticide_data, load_yield_data
import plotly.express as px
from prediction_tab import prediction_tab

# Load datatsets
pesticide_df = load_pesticide_data()
yield_df = load_yield_data()
unique_years = sorted(yield_df["Year"].dropna().unique())


def register_callbacks(app): #Register all callbacks for the dash app
    @app.callback(
        Output("tab-content", "children"),
        Input("tabs", "value") #updataing main conent area when tab is clicked
    )
    def switch_tabs(tab_name): #switch tabs
        if tab_name == "dashboard-tab":
            return dashboard_tab
        elif tab_name == "map-tab":
            return map_tab
        elif tab_name == "heatmap-tab":
            return heatmap_tab
        elif tab_name == "prediction-tab":
            return prediction_tab

    @app.callback( #Updates Graphs
        Output("graph-output", "figure"),
        Input("view-selector", "value"),
        Input("year-selector", "value")
    )
    def update_graph(view, year):     # Line chart for national pesticide consumption
        if view == "pesticide":
            fig = px.line(
                pesticide_df,
                x="YEAR",
                y="Quantity (M.T) Total",
                title="Pesticide Consumption in Pakistan"
            )
        else:             # Bar chart of wheat yield by district for selected year
            filtered = yield_df[yield_df["Year"] == year]
            fig = px.bar(
                filtered,
                x="District",
                y="Yield",
                title=f"Wheat Yield by District ({year})"
            )
        return fig

    # Register heatmap callbacks
    register_heatmap_callbacks(app)