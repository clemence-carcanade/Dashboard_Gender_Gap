#IMPORT
import dash
import plotly.express as px
from dash import Dash, Input, Output, html, dcc
import geopandas as gpd
import json
import pandas as pd

#Travail préalable : Recherche des données manquantes 
#Recherche de données manquante pour des pays 
df = pd.read_csv("../../../data/raw/women_in_stem.csv")
world = gpd.read_file("../../../data/raw/world_boundaries.geojson")
with open("../../../data/raw/world_boundaries.geojson") as f:
    world_geojson = json.load(f)
app = dash.Dash(__name__)



years = df["Year"].unique()
stem=df["STEM Fields"].unique()

colorscale= [     
        [0, "#fff0f3"],
        [0.1, "#ffb3c1"],
        [0.2, "#ff8fa3"],
        [0.3, "#ff758f"],
        [0.4, "#ff4d6d"],
        [0.5, "#c9184a"],
        [0.6, "#a4133c"],
        [0.7, "#800f2f"],
        [1.0, "#590d22"]
    ]
 
app.layout = html.Div([
    html.Label("Sélectionnez une année et une discipline:",style={
    "font-size": "24px",
    "font-weight": "600",
    "color": "#410919",
    "margin-bottom": "15px",
    "letter-spacing": "0.5px"
}),

    dcc.Dropdown(
        id='year-dropdown',
        options=[{"label": str(y), "value": y} for y in years],
        value=2022,
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
        id='stem-dropdown',
        options=[{"label": str(y), "value": y} for y in stem],
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

@app.callback(
    Output('histogram', 'figure'),
    [Input('year-dropdown', 'value'), Input('stem-dropdown', 'value')]
)

def update_map(selected_year, selected_stem):
    df_filtre= df[df["Year"] == selected_year]
    if selected_stem != "All":
        df_filtre = df_filtre[df_filtre["STEM Fields"] == selected_stem]
    
    df_agg = df_filtre.groupby(['Country', 'STEM Fields'], as_index=False).agg({
        'Female Graduation Rate': 'mean'
    })

    fig = px.bar(
        df_agg,
        y='Country',
        x='Female Graduation Rate',
        color_continuous_scale=colorscale,
        labels={'Female Graduation Rate': 'Taux de diplômées', 'Country': 'Pays', 'STEM Fields':'Discipline scientifique'},
        color='Female Graduation Rate',
        hover_data=['STEM Fields']
        )
   
    return fig 


app.run(debug=True)
