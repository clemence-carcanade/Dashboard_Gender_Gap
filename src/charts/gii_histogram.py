import plotly.express as px
from dash import Input, Output, html, dcc, callback
import pandas as pd

df = pd.read_csv("data/raw/world_GII.csv")

gii_columns = [col for col in df.columns if col.startswith("Gender Inequality Index")]

df_long = df.melt(
    id_vars=["ISO3", "Country", "Continent"],
    value_vars=gii_columns,
    var_name="Year",
    value_name="GII"
)

df_long['Year'] = df_long['Year'].str.extract(r'(\d{4})').astype(int)
df_long = df_long.dropna(subset=['GII'])
years = sorted(df_long["Year"].unique())
continent = ["All"] + sorted(df_long["Continent"].dropna().unique())

colorscale = [
    [0.0, "#F5F5F5"],
    [0.00001, "#FBEAF4"],
    [0.1, "#F4C3E0"],
    [0.2, "#EDA1CE"],
    [0.3, "#E576B8"],
    [0.4, "#DE4FA5"],
    [0.5, "#D62991"],
    [0.6, "#B02177"],
    [0.7, "#891A5D"],
    [1.0, "#631343"],
]

def layout():
    return html.Div(
        className="gii_data_container",
        children=[
        html.Label(
            "Sélectionnez une année et un continent :",
            style={
                "font-size": "24px",
                "font-weight": "600",
                "color": "#410919",
                "margin-bottom": "15px",
                "letter-spacing": "0.5px"
            }
        ),

        dcc.Dropdown(
            id='year-dropdown',
            options=[{"label": str(y), "value": y} for y in years],
            value=2021,
            clearable=False,
            searchable=False,
            style={
                "font-size": "20px",
                "font-weight": "500",
                "color": "#590d22",
                "margin-bottom": "10px",
                "border-left": "4px solid #590d22",
                "padding-left": "12px"
            }
        ),

        dcc.Dropdown(
            id='continent-dropdown',
            options=[{"label": str(y), "value": y} for y in continent],
            value="All",
            clearable=False,
            searchable=False,
            style={
                "font-size": "20px",
                "font-weight": "500",
                "color": "#590d22",
                "margin-bottom": "10px",
                "border-left": "4px solid #590d22",
                "padding-left": "12px"
            }
        ),

        dcc.Graph(id='histogram'),
    ])

@callback(
    Output('histogram', 'figure'),
    [Input('year-dropdown', 'value'), Input('continent-dropdown', 'value')]
)
def update_map(selected_year, selected_continent):
    df_filtre= df_long[df_long["Year"] == selected_year]
    if selected_continent != "All":
        df_filtre = df_filtre[df_filtre["Continent"] == selected_continent]
    fig = px.bar(
        df_filtre,
        x='Country',
        y='GII',
        labels={'GII': 'GII', 'Country': 'Pays'},
        color='GII',
        color_continuous_scale=colorscale,
        hover_data=['Continent']
        )
    fig.update_layout(
        xaxis_tickangle=-45,
        height=600,
        showlegend=False
    )
    return fig 