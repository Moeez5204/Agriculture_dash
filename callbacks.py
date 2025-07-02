from dash import Input, Output, html, dcc
import plotly.express as px
from data_loader import load_pesticide_data, load_yield_data

pesticide_df = load_pesticide_data()
yield_df = load_yield_data()

def register_callbacks(app):
    @app.callback(
        Output("graph-output", "children"),
        Input("view-selector", "value"),
        Input("year-selector", "value")
    )
    def update_graph(view, selected_year):
        if view == "pesticide":
            return [
                dcc.Graph(figure=px.line(
                    pesticide_df,
                    x="YEAR",
                    y=["Quantity (M.T) Imports", "Quantity (M.T) Production", "Quantity (M.T) Total"],
                    title="Pesticide Imports, Production & Total"
                )),
                dcc.Graph(figure=px.bar(
                    pesticide_df,
                    x="YEAR",
                    y="Value (Million Rs.)",
                    title="Pesticide Value in Rs"
                ))
            ]
        elif view == "yield":
            filtered = yield_df[yield_df["Year"] == selected_year]
            return dcc.Graph(figure=px.bar(
                filtered.sort_values("Yield", ascending=False),
                x="District",
                y="Yield",
                title=f"Wheat Yield by District – {selected_year}",
                labels={"Yield": "Yield"}
            ))
        return html.Div("No data available.")