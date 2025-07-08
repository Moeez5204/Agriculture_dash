import pandas as pd
import plotly.express as px
from dash import html,dcc


forecast_df = pd.read_csv('outputs/Punjab_Yield_Forecast.csv')
actual_df = pd.read_csv('Data/Wheat_Yield_Punjab_2020_2023.csv')