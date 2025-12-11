#IMPORT
import dash
import plotly.express as px
from dash import Dash, Input, Output, html, dcc
import geopandas as gpd
import json
import pandas as pd

#Travail préalable : Recherche des données manquantes 
#Recherche de données manquante pour des pays 
df = pd.read_csv("../../../data/raw/world_research_women.csv")
world = gpd.read_file("../../../data/raw/countries.geojson")
with open("../../../data/raw/countries.geojson") as f:
    world_geojson = json.load(f)

#Filtrer les regions /groupes pour qu'il n'y ait que des codes de pays
# Liste des préfixes à exclure
regional_prefixes = ['SDG:', 'UIS:', 'MDG:', 'WB:', 'UNESCO:']

# Fonction pour identifier si c'est un code régional
def is_regional_code(code):
    return any(code.startswith(prefix) for prefix in regional_prefixes) #donner par IA

# Filtrer le DataFrame pour garder UNIQUEMENT les pays
df_countries = df[~df['geoUnit'].apply(is_regional_code)] #donner par IA

gii_codes = set(df_countries['geoUnit'].unique())
geo_codes = set(world['ISO3166-1-Alpha-3'].unique())

#On veut afficher les noms des pays donc on prends les nom sur le geojson puisque non present sur le fichier csv
#print("Colonnes du GeoJSON :", world.columns.tolist())
df_countries = df_countries.merge(
    world[['ISO3166-1-Alpha-3', 'name']],
    left_on='geoUnit',
    right_on='ISO3166-1-Alpha-3',
    how='left'
).rename(columns={'name': 'Country'})

#missing_in_geojson = gii_codes - geo_codes
#print(missing_in_geojson)

#missing_in_gii = geo_codes - gii_codes
#print(missing_in_gii)

#gii_codes = set(df['geoUnit'].unique())
#print(len(gii_codes)) #NBRE DE PAYS

#df_year_2020=df_long[df_long['Year'] == 2020] 
#DATA
#Passage format wide au format long
#DASH

app = dash.Dash(__name__)

#Pas besoin de changer le format --> le fichier csv est déjà au format long

years = sorted(df_countries["year"].unique())   
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

    dcc.Graph(id='map'),
])

@app.callback(
    Output('map', 'figure'),
    Input('year-dropdown', 'value')
)

def update_map(selected_year):
    df_year = df_countries[df_countries["year"] == selected_year]
    # Merge à l'intérieur du callback
    merged_df = world.merge(
        df_year,
        left_on='ISO3166-1-Alpha-3',
        right_on='geoUnit',
        how='outer'
    )
    print(merged_df.columns)
    #Code pour grisé les pays non reconnu -- > difficulté donc sollicite l'IA
    # si la colonne 'ISO3' existe (données), on la prend, sinon on prend 'ISO_A3' du GeoDataFrame
    merged_df['plot_iso'] = merged_df['geoUnit'].fillna(merged_df['ISO3166-1-Alpha-3_x'])
    #skipna=on ignore les NaN et on cherche la plus petite valeur du GII 
    #afin de plus tard créer une valeur artificielle encore plus petite pour faire apparaître les pays grisé
    #même principe pour les valeurs max
    real_min = df_countries['value'].min(skipna=True)
    real_max = df_countries['value'].max(skipna=True)
    #on prends la plus petitre valeur réelle et on descend légèrement en dessous
    sentinel = real_min - (abs(real_min) * 0.1 + 0.01) 
    #on créer une nouvelle version : tous les NaN sont remplacés par des sentinels pour au final retirer tous les NaN
    merged_df['value_plot'] = merged_df['value'].fillna(sentinel)
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
        color='value_plot',   
        hover_name='Country',
        hover_data={
            'plot_iso': False,      # Cache le code ISO
            'value_plot': ':.3f'    # Affiche la valeur avec 3 décimales
        },
        featureidkey='properties.ISO3166-1-Alpha-3',
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
