#IMPORT
import dash
import plotly.express as px
from dash import Dash, Input, Output, html, dcc
import geopandas as gpd
import json
import pandas as pd

#Travail préalable : Recherche des données manquantes 
#Recherche de données manquante pour des pays 

#gii_codes = set(df_long['ISO3'].unique())
#geo_codes = set(world['iso3'].unique())

#missing_in_geojson = gii_codes - geo_codes
#print(missing_in_geojson)

#missing_in_gii = geo_codes - gii_codes
#print(missing_in_gii)

#gii_codes = set(df_long['ISO3'].unique())
#print(len(gii_codes)) NBRE DE PAYS

#df_year_2020=df_long[df_long['Year'] == 2020] 
#DATA
#Passage format wide au format long
#DASH

#Lecture des données et carte
df = pd.read_csv("../../../data/raw/world_GII.csv")
world = gpd.read_file("../../../data/raw/world_boundaries.geojson")
with open("../../../data/raw/world_boundaries.geojson") as f:
    world_geojson = json.load(f)

app = dash.Dash(__name__)

#Code couleur pour la cart

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

#Mise en place du slider
years = df_long["Year"].unique()
app.layout = html.Div([
    html.Label("Sélectionnez une année :",style={
    "font-size": "24px",
    "font-weight": "600",
    "color": "#410919",
    "margin-bottom": "15px",
    "letter-spacing": "0.5px"
}),

    dcc.Dropdown(
        id='year-dropdown',
        options=[{"label": str(y), "value": y} for y in sorted(years)],
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

    dcc.Graph(id='map'),
])

@app.callback(
    Output('map', 'figure'),
    Input('year-dropdown', 'value')
)

def update_map(selected_year):
    df_year = df_long[df_long["Year"] == selected_year]
    # Merge à l'intérieur du callback
    merged_df = world.merge(
        df_year,
        left_on='iso3',
        right_on='ISO3',
        how='outer'
    )
    #Code pour grisé les pays non reconnu -- > difficulté donc sollicite l'IA
    # si la colonne 'ISO3' existe (données), on la prend, sinon on prend 'iso3' du GeoDataFrame
    merged_df['plot_iso'] = merged_df['ISO3'].fillna(merged_df['iso3'])
    #skipna=on ignore les NaN et on cherche la plus petite valeur du GII 
    #afin de plus tard créer une valeur artificielle encore plus petite pour faire apparaître les pays grisé
    #même principe pour les valeurs max
    real_min = df_long['GII'].min(skipna=True)
    real_max = df_long['GII'].max(skipna=True)
    #on prends la plus petitre valeur réelle et on descend légèrement en dessous
    sentinel = real_min - (abs(real_min) * 0.1 + 0.01) 
    #on créer une nouvelle version : tous les NaN sont remplacés par des sentinels pour au final retirer tous les NaN
    merged_df['GII_plot'] = merged_df['GII'].fillna(sentinel)

    colorscale_with_grey = [
        [0.0, "lightgrey"],      
        [0.00001, "#fff0f3"],
        [0.1, "#ffb3c1"],
        [0.2, "#ff8fa3"],
        [0.3, "#ff758f"],
        [0.4, "#ff4d6d"],
        [0.5, "#c9184a"],
        [0.6, "#a4133c"],
        [0.7, "#800f2f"],
        [1.0, "#590d22"]
    ]

    fig = px.choropleth(
        merged_df,
        geojson=world_geojson,
        locations='plot_iso',            # colonne contenant les ISO valides pour tous les pays et ne prends donc plus en compte les NaN
        color='GII_plot',   
        hover_name='Country',
        featureidkey='properties.iso3',
        projection='natural earth',
        color_continuous_scale=colorscale_with_grey,
        )
    # Ajouter des frontières visibles
    fig.update_traces(
        marker_line_color="#dfdfdd",   # couleur des frontières
        marker_line_width=0.9        # épaisseur des frontières
    )

    #Mise en forme de la carte : A MODIFIER pour intégration sur la page dashboard    
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig  


app.run(debug=True)


