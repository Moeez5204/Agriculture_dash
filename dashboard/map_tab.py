from dash import html, dcc, Input, Output, callback
import plotly.express as px
from data_loader import prepare_volatility_data

# Prepare data
coord_df, vol_df = prepare_volatility_data()

# Get unique years for dropdown
available_years = sorted(vol_df['Year'].unique())

# Dash layout for the tab
map_tab = html.Div([
    html.H4("Punjab Wheat Yield Volatility by Year"),

    # Year selector dropdown
    html.Div([
        html.Label("Select Year:", style={'margin-right': '10px'}),
        dcc.Dropdown(
            id='year-selector',
            options=[{'label': str(year), 'value': year} for year in available_years],
            value=available_years[-1],  # Default to most recent year
            clearable=False,
            style={'width': '150px', 'display': 'inline-block'}
        )
    ], style={'margin-bottom': '20px'}),

    # Map graph
    dcc.Graph(id="district-map"),

    html.Hr(style={"marginTop": "20px", "marginBottom": "20px"}),

    # Volatility categories section
    html.Div(id='volatility-categories')
])


# Callback to update map and categories based on selected year
@callback(
    [Output('district-map', 'figure'),
     Output('volatility-categories', 'children')],
    [Input('year-selector', 'value')]
)
def update_map(selected_year):
    # Filter data for selected year
    year_data = coord_df[coord_df['Year'] == selected_year]

    # Create map figure
    fig = px.scatter_mapbox(
        year_data,
        lat="Latitude",
        lon="Longitude",
        hover_name="District",
        hover_data={"Yield_StdDev": ":.2f", "Volatility_Level": True},
        color="Volatility_Level",
        color_discrete_map={
            "Low": "green",
            "Medium": "orange",
            "High": "red"
        },
        zoom=6.5,
        height=600
    )

    # Customize map
    fig.update_traces(
        marker=dict(size=12),
        hovertemplate="District: %{hovertext}<br>Volatility: %{customdata[0]:.2f} T/Ha<br>Level: %{customdata[1]}<extra></extra>"
    )
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        showlegend=False
    )

    # Prepare volatility categories for selected year
    year_vol = vol_df[vol_df['Year'] == selected_year]
    low_districts = year_vol[year_vol["Volatility_Level"] == "Low"]["District"].sort_values().tolist()
    med_districts = year_vol[year_vol["Volatility_Level"] == "Medium"]["District"].sort_values().tolist()
    high_districts = year_vol[year_vol["Volatility_Level"] == "High"]["District"].sort_values().tolist()

    categories_div = html.Div([
        html.H4(f"Districts Grouped by Volatility ({selected_year})"),

        html.Div([
            html.H5("Low Volatility"),
            html.Ul([html.Li(district) for district in low_districts])
        ], style={"width": "30%", "display": "inline-block", "verticalAlign": "top"}),

        html.Div([
            html.H5("Medium Volatility"),
            html.Ul([html.Li(district) for district in med_districts])
        ], style={"width": "30%", "display": "inline-block", "verticalAlign": "top"}),

        html.Div([
            html.H5("High Volatility"),
            html.Ul([html.Li(district) for district in high_districts])
        ], style={"width": "30%", "display": "inline-block", "verticalAlign": "top"})
    ])

    return fig, categories_div