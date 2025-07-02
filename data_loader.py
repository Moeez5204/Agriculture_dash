import pandas as pd

def load_pesticide_data():
    df = pd.read_csv("Pesticide Consumption Pakistan 2008-2018.csv")
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).str.replace(",", "").astype(int)
    return df

def load_yield_data():
    df = pd.read_csv("Wheat Yield by Districts Punjab.csv")
    df.rename(columns={df.columns[0]: "District"}, inplace=True)
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", ""), errors="coerce")
    return df.melt(id_vars="District", var_name="Year", value_name="Yield")