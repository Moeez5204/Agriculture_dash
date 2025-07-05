import pandas as pd
from dash import Input, Output, html
from dashboard_tab import dashboard_tab
from map_tab import map_tab
from data_loader import load_pesticide_data, load_yield_data
import plotly.express as px
#Callbacks
pesticide_df = load_pesticide_data()
yield_df = load_yield_data()
unique_years = sorted(yield_df["Year"].dropna().unique())
#forecast_df = pd.read_csv("outputs/Punjab_Yield_Forecast.csv")
def register_callbacks(app):
    @app.callback(
        Output("tab-content", "children"),
        Input("tabs", "value")
    )
    def switch_tabs(tab_name):
        if tab_name == "dashboard-tab":
            return dashboard_tab
        elif tab_name == "map-tab":
            return map_tab
    @app.callback(
        Output("graph-output", "figure"),
        Input("view-selector", "value"),
        Input("year-selector", "value")
    )
    def update_graph(view, year):
        if view == "pesticide":
            fig = px.line(
                pesticide_df,
                x="YEAR",
                y="Quantity (M.T) Total",
                title="Pesticide Consumption in Pakistan"
            )
        else:
            filtered = yield_df[yield_df["Year"] == year]
            fig = px.bar(
                filtered,
                x="District",
                y="Yield",
                title=f"Wheat Yield by District ({year})"
            )
        return fig