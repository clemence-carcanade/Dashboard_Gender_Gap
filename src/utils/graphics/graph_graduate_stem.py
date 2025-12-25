#IMPORT
import dash
import plotly.express as px
from dash import Dash, Input, Output, State, html, dcc, ctx
import geopandas as gpd
import json
import pandas as pd

df = pd.read_csv("../../../data/raw/share-graduates-stem-female.csv")

app = dash.Dash(__name__)


VALUE_COL = 'Female share of graduates from Science, Technology, Engineering and Mathematics (STEM) programmes, tertiary'
years = sorted(df["Year"].unique())
GLOBAL_MIN = df[VALUE_COL].min() #valeur min pour la légende
GLOBAL_MAX = df[VALUE_COL].max() #valeur max pour la légende
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
    dcc.Interval(   id='interval',
                    interval=800, # in milliseconds
                    n_intervals=0,
                    disabled=True),

    dcc.Slider(id="year-slider",
                min=int(min(years)),
                max=int(max(years)),
                step=1,
                marks={int(y): str(y) for y in years},
                value=years[0]),

    dcc.Dropdown(
        id='year-dropdown',
        options=[{"label": str(y), "value": y} for y in years],
        value=years[0],
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
    id='country-selector',
    options=[
        {"label": c, "value": c}
        for c in sorted(df['Entity'].unique())
    ],
    value=[],
    multi=True,
    placeholder="Sélectionnez des pays (optionnel)"
    ),

    #Store pour garder l'état
    dcc.Store(id='animation-state', data={'playing': False, 'start_year': years[0]}),

    dcc.Graph(id='histogram'),
    html.Div(
       children=[
       html.Button('PLAY', id='btn-play', n_clicks=0),
       html.Button('PAUSE', id='btn-pause', n_clicks=0),
                ]
        )
])
@app.callback(  [Output('year-slider', 'value'), Output('interval', 'disabled'), 
                 Output('animation-state', 'data')],
                [Input('interval', 'n_intervals'), Input('btn-play', 'n_clicks'),  # bouton PLAY
                Input('btn-pause', 'n_clicks'), Input('year-dropdown', 'value'),
                Input('year-slider', 'value')],
                [State('animation-state', 'data')])

#FONCTION A REVOIR
def animation(n_intervals, play_clicks, pause_clicks, dropdown_year, slider_year, state):
    """
    Gère l'animation et les contrôles de lecture
    
    Returns:
        tuple: (année du slider, interval désactivé?, état de l'animation)
    """
    # Identifier quel composant a déclenché le callback
    triggered_id = ctx.triggered_id
    
    # Initialisation du state si nécessaire
    if state is None:
        state = {'playing': False, 'start_year': years[0]}
    
    # Gestion de l'appel initial (au chargement de la page)
    if triggered_id is None:
        return years[0], True, state
    
    # --- INTERACTIONS UTILISATEUR ---
    
    # L'utilisateur sélectionne une année dans le dropdown
    if triggered_id == 'year-dropdown':
        state['start_year'] = dropdown_year
        return dropdown_year, True, {**state, 'playing': False}
    
    # L'utilisateur déplace le slider manuellement
    if triggered_id == 'year-slider':
        state['start_year'] = slider_year
        return slider_year, True, {**state, 'playing': False}
    
    # L'utilisateur clique sur PLAY
    if triggered_id == 'btn-play':
        state['playing'] = True
        # Démarrer depuis l'année actuelle du slider
        return slider_year, False, state
    
    # L'utilisateur clique sur PAUSE
    if triggered_id == 'btn-pause':
        state['playing'] = False
        return slider_year, True, state
    
    # --- ANIMATION AUTOMATIQUE ---
    
    # L'interval "tick" et l'animation est en cours
    if triggered_id == 'interval' and state.get('playing', False):
        # Trouver l'index de l'année actuelle
        try:
            current_index = years.index(slider_year)
        except ValueError:
            # En cas d'erreur, revenir au début
            current_index = 0
        
        # Calculer l'année suivante
        next_index = current_index + 1
        
        # Vérifier si on a atteint la fin
        if next_index >= len(years):
            # Arrêter l'animation à la dernière année
            return years[-1], True, {**state, 'playing': False}
        
        # Passer à l'année suivante
        new_year = years[next_index]
        return new_year, False, state
    
    #    Aucun changement nécessaire
    return dash.no_update, dash.no_update, dash.no_update


@app.callback(
    Output('histogram', 'figure'),
     [Input('country-selector', 'value'),
    Input('year-slider', 'value')]
)

def update_map(selected_countries, selected_year):
    df_year = df[df['Year'] == selected_year]
    # Liste complète et stable des pays
    if selected_countries:
        df_year = df_year[df_year['Entity'].isin(selected_countries)]

    fig = px.bar(
        df_year,
        y='Entity',
        x=VALUE_COL,
        color_continuous_scale=colorscale,
        range_color=[GLOBAL_MIN, GLOBAL_MAX],
        labels={VALUE_COL: 'Taux de diplômées', 'Entity': 'Pays'},
        color=VALUE_COL,
        hover_data=[VALUE_COL]
        )
    fig.update_layout(
    transition=dict(
        duration=500,
        easing='cubic-in-out'
    )
)
   
    return fig 


app.run(debug=True)
