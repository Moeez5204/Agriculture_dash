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


def load_pesticide_data():
    df = pd.read_csv("data/Pesticide Consumption Pakistan 2008-2018.csv")
    df.columns = df.columns.str.strip()
    df = clean_numeric_column(df, "Quantity (M.T) Total")
    df.dropna(subset=["Quantity (M.T) Total"], inplace=True)
    return df


def load_yield_data():
    df = pd.read_csv("data/Wheat Yield by Districts Punjab.csv")
    df.columns = df.columns.str.strip()
    df.rename(columns={df.columns[0]: "District"}, inplace=True)

    # Melt from wide to long format
    df_long = df.melt(id_vars="District", var_name="Year", value_name="Yield")

    # Clean Yield values and Year
    df_long["Yield"] = (
        df_long["Yield"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("**", "", regex=False)
        .str.strip()
    )
    df_long["Yield"] = pd.to_numeric(df_long["Yield"], errors="coerce")
    df_long.dropna(subset=["Yield"], inplace=True)

    # Convert Year to numeric (assuming format like "2008-09")
    df_long['Year'] = df_long['Year'].str.split('-').str[0].astype(int)

    return df_long


def compute_yearly_volatility(df, window=3):
    """Compute rolling volatility (std dev) for each district with given window size"""
    vol_df = df.sort_values(['District', 'Year'])
    vol_df['Yield_StdDev'] = vol_df.groupby('District')['Yield'].transform(
        lambda x: x.rolling(window, min_periods=1).std()
    )
    return vol_df


def categorize_volatility(df):
    """Add volatility level column based on yearly percentiles"""
    # Calculate yearly percentiles
    yearly_percentiles = df.groupby('Year')['Yield_StdDev'].quantile([1 / 3, 2 / 3]).unstack()
    yearly_percentiles.columns = ['low_thres', 'high_thres']

    # Merge percentiles back to main df
    df = df.merge(yearly_percentiles, on='Year')

    # Categorize
    df['Volatility_Level'] = 'Medium'
    df.loc[df['Yield_StdDev'] <= df['low_thres'], 'Volatility_Level'] = 'Low'
    df.loc[df['Yield_StdDev'] > df['high_thres'], 'Volatility_Level'] = 'High'

    return df.drop(columns=['low_thres', 'high_thres'])


def prepare_volatility_data():
    """Main function to prepare all volatility data"""
    yield_df = load_yield_data()
    vol_df = compute_yearly_volatility(yield_df)
    vol_df = categorize_volatility(vol_df)

    # Merge with coordinates
    coord_df = pd.read_csv("data/Punjab_District_Coord.csv")
    coord_df = coord_df.merge(vol_df, on="District", how="left")

    return coord_df, vol_df