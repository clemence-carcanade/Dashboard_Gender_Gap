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
app = dash.Dash(__name__)

df = pd.read_csv("../../../data/raw/world_GII.csv")
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

years = df_long["Year"].unique()

app.layout = html.Div([
    dcc.Slider(
        df_long["Year"].min(),
        df_long["Year"].max(),
        step=None,
        value=2020,
        marks={str(y): str(y) for y in years},
        id='year-slider'
    ),
    dcc.Graph(id='map')
])

@app.callback(
    Output('map', 'figure'),
    Input('year-slider', 'value')
)
def update_map(selected_year):
    df_year = df_long[df_long["Year"] == selected_year]

world = gpd.read_file("../../../data/raw/world_boundaries.geojson")


#Recherche de données manquante pour des pays 

#gii_codes = set(df_long['ISO3'].unique())
#geo_codes = set(world['iso3'].unique())

#missing_in_geojson = gii_codes - geo_codes
#print(missing_in_geojson)

#missing_in_gii = geo_codes - gii_codes
#print(missing_in_gii)

#gii_codes = set(df_long['ISO3'].unique())
#print(len(gii_codes)) NBRE DE PAYS

df_year_2020=df_long[df_long['Year'] == 2020]   

with open("../../../data/raw/world_boundaries.geojson") as f:
    world_geojson = json.load(f)

# Fusionner la carte du monde avec données
merged_df = world.merge(
    df_year_2020,
    left_on='iso3',   
    right_on='ISO3',  
    how='outer'        
)
colorscale = [
    [0.0, "lightgrey"],   # pays sans données (NaN)
    [0.01, "#f7c6d0"],    # valeur faible → rose très clair
    [0.3, "#e39cb0"],     # intermédiaire clair
    [0.5, "#d17796"],     # intermédiaire moyen
    [0.7, "#bb5e88"],     # intermédiaire foncé
    [1.0, "#b86485"]      # valeur maximale → ton rose choisi
]
fig = px.choropleth(
    merged_df,
    geojson=world_geojson,       
    locations='ISO3',            
    color='GII',
    hover_name='Country',
    featureidkey='properties.iso3', 
    projection='natural earth',
    color_continuous_scale=colorscale,
)

fig.update_geos(fitbounds="locations", visible=False)
fig.show()


