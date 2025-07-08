import pandas as pd
import plotly.express as px
from dash import html, dcc

# Load the forecast and actual yield data
forecast_df = pd.read_csv('/Users/abdul-moeez/PycharmProjects/Dashboard/outputs/Punjab_Yield_Forecast.csv')
actual_df = pd.read_csv('/Users/abdul-moeez/PycharmProjects/Dashboard/Data/Wheat_Yield_Punjab_2020_2023.csv')

# Prep actual data
actual_long = actual_df.melt(
    id_vars=actual_df.columns[0],
    var_name="Year",
    value_name="Yield"
)

# Clean actual data
actual_long["Yield"] = (
    actual_long["Yield"].astype(str)
    .str.replace(",", "")
    .str.replace("**", "")
    .str.extract(r"(\d+)")
)
actual_long["Yield"] = pd.to_numeric(actual_long["Yield"], errors="coerce")
actual_long = actual_long.dropna(subset=["Yield"])
actual_avg = actual_long.groupby("Year", as_index=False)["Yield"].mean()

# Standardize year format
actual_avg["Year"] = actual_avg["Year"].astype(str).str.extract(r"(\d{4})")
actual_avg["Year"] = pd.to_numeric(actual_avg["Year"], errors="coerce")
forecast_df["Year"] = forecast_df["Year"].astype(int)

# Add rolling average to smooth the predictions
forecast_df = forecast_df.sort_values("Year")
forecast_df["Smoothed"] = forecast_df["Predicted Yield"].rolling(window=2, min_periods=1).mean()

# Split for plotting: Actual = 2000–2023, Predicted = 2024 onward
actual_plot = forecast_df[forecast_df["Year"] <= 2023].copy()
predicted_plot = forecast_df[forecast_df["Year"] >= 2024].copy()

actual_plot["Type"] = "Actual"
predicted_plot["Type"] = "Predicted"
predicted_plot["Yield"] = predicted_plot["Smoothed"]
actual_plot["Yield"] = actual_plot["Smoothed"]

# Combine both parts
combined_df = pd.concat([actual_plot, predicted_plot])
combined_df["Year"] = combined_df["Year"].astype(str)

# Plot
fig = px.line(
    combined_df,
    x="Year", y="Yield", color="Type",
    color_discrete_map={"Actual": "blue", "Predicted": "red"},
    title="Punjab Wheat Yield: Actual (2000–2023) vs Predicted (2024–2028)",
    markers=True
)
fig.update_traces(mode="lines+markers")

# Layout
prediction_tab = html.Div([
    html.H3("Yield Prediction vs Actual Data"),
    dcc.Graph(figure=fig)
])