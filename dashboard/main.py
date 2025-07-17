from dash import Dash
import dash_bootstrap_components as dbc
from layout import layout
from callbacks import register_callbacks

#main
#Combines all data together

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "Wheat & Pesticide Dashboard"
app.layout = layout

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)