#IMPORT
import dash
import plotly.express as px
from dash import Dash, Input, Output, html, dcc
import geopandas as gpd
import json
import pandas as pd

#DATA
#Passage format wide au format long
#DASH

#Lecture des données et carte
df = pd.read_csv("../../../data/raw/world_GII.csv")

app = dash.Dash(__name__)

gii_columns = []    
for col in df.columns :
    if col.startswith("Gender Inequality Index") :
        gii_columns.append(col)

df_long = df.melt(
    id_vars=['ISO3', 'Country', 'Continent'],  
    value_vars=gii_columns,                                  
    var_name='Year',                                         
    value_name='GII'                                         
)
df_long['Year'] = df_long['Year'].str.extract(r'(\d{4})').astype(int) #Ligne donné par IA pour extraire l'année et non Gender Inequality Index (1990)
df_long = df_long.dropna(subset=['GII']) #dropna sert à supprimer les valeurs manquantes (NaN)
years = sorted(df_long["Year"].unique())
continent = sorted(df_long["Continent"].dropna().unique()) 
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
    html.Label("Sélectionnez une année et un continent :",style={
    "font-size": "24px",
    "font-weight": "600",
    "color": "#410919",
    "margin-bottom": "15px",
    "letter-spacing": "0.5px"
}),

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

@app.callback(
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
        labels={'GII': 'Gender Inequality Index', 'Country': 'Pays'},
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
 


app.run(debug=True)
    