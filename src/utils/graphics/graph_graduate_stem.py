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
    dcc.Graph(id='histogram')
])
@app.callback(
    Output('histogram', 'figure'),
    Input('year-dropdown', 'value')
)

def update_map(selected_year):
    df_filtre= df[df["Year"] == selected_year]
    fig = px.bar(
        df_filtre,
        x='Entity',
        y=VALUE_COL,
        labels={'Female share of graduates from Science, Technology, Engineering and Mathematics (STEM) programmes, tertiary': 'Female share of graduates'+ '\n'+ 'in STEM programmes', 'Entity': 'Countries'},
        color='Female share of graduates from Science, Technology, Engineering and Mathematics (STEM) programmes, tertiary',
        color_continuous_scale=colorscale,
        hover_data=['Entity']
        )
    fig.update_layout(
        xaxis_tickangle=-45,
        height=600,
        showlegend=False
    )
    return fig 
 


app.run(debug=True)
    