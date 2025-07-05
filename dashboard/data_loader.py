# data_loader
import pandas as pd

# Utility function to clean numeric columns
def clean_numeric_column(df, column_name):
    df[column_name] = (
        df[column_name]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df[column_name] = pd.to_numeric(df[column_name], errors="coerce")
    return df

#data_loader
def load_pesticide_data():
    df = pd.read_csv("data/Pesticide Consumption Pakistan 2008-2018.csv")
    df.columns = df.columns.str.strip()

    # Clean quantity column: remove commas and convert to numeric
    df = clean_numeric_column(df, "Quantity (M.T) Total")

    # Drop any rows with missing values in the quantity
    df.dropna(subset=["Quantity (M.T) Total"], inplace=True)
    return df

def load_yield_data():
    df = pd.read_csv("data/Wheat Yield by Districts Punjab.csv")
    df.columns = df.columns.str.strip()

    # Rename the first column to "District"
    df.rename(columns={df.columns[0]: "District"}, inplace=True)

    # Melt from wide to long format
    df_long = df.melt(id_vars="District", var_name="Year", value_name="Yield")

    # Clean Yield values
    df_long["Yield"] = (
        df_long["Yield"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("**", "", regex=False)
        .str.strip()
    )
    df_long["Yield"] = pd.to_numeric(df_long["Yield"], errors="coerce")
    # Drop invalid rows
    df_long.dropna(subset=["Yield"], inplace=True)

    return df_long

