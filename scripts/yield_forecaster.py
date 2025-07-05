# scripts/yield_forecaster.py

import os
import sys
import pandas as pd
from pathlib import Path
from prophet import Prophet

# Add dashboard/ to import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dashboard.data_loader import load_yield_data

# Make sure we are in the project root so relative paths work
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Define output path
OUTPUT_PATH = Path("outputs/Punjab_Yield_Forecast.csv")

def forecast_punjab_yield():
    df = load_yield_data()
    year_avg = df.groupby("Year", as_index=False)["Yield"].mean()

    # Prepare for Prophet
    df_prophet = year_avg.rename(columns={"Year": "ds", "Yield": "y"})

    # ✅ Clean up the ds column (just 4-digit years)
    df_prophet["ds"] = df_prophet["ds"].astype(str).str.extract(r"(\d{4})")
    df_prophet["ds"] = pd.to_datetime(df_prophet["ds"], format="%Y")

    # Fit model
    model = Prophet()
    model.fit(df_prophet)

    # Forecast next 10 years
    future = model.make_future_dataframe(periods=10, freq="Y")
    forecast = model.predict(future)

    # Clean output
    result = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].copy()
    result["ds"] = result["ds"].dt.year
    result = result.rename(columns={
        "ds": "Year",
        "yhat": "Predicted Yield",
        "yhat_lower": "Lower Bound",
        "yhat_upper": "Upper Bound"
    })

    # Save to CSV
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_PATH, index=False)

    return result

if __name__ == "__main__":
    df = forecast_punjab_yield()
    print(df.tail())
    print(f" Saved forecast to: {OUTPUT_PATH}")