# IMPORTS
import plotly.express as px
from dash import html, dcc, Input, Output, callback
import pandas as pd
import csv

# --- Lecture du CSV ---
with open(
    "data/raw/fr_research_women_feuille2.csv",
    newline="",
    encoding="utf-8"
) as fichier:
    lecteur = csv.reader(fichier)
    lignes = list(lecteur)

# Repérer la ligne d'en-tête contenant les années
for i, ligne in enumerate(lignes):
    if "2010-2011" in ligne and "2020-2021" in ligne:
        index_header = i
        break

# Indices des colonnes
col_discipline = 0
col_2010 = lignes[index_header].index("2010-2011")
col_2020 = lignes[index_header].index("2020-2021")

# Extraction des données
data = []
for ligne in lignes[index_header + 1:]:
    try:
        if ligne[col_2010] and ligne[col_2020]:
            data.append({
                "discipline": ligne[col_discipline],
                "2010-2011": float(ligne[col_2010]),
                "2020-2021": float(ligne[col_2020]),
            })
    except (ValueError, IndexError):
        continue

df = pd.DataFrame(data)
years = ["2010-2011", "2020-2021"]

# --- Couleurs du graphique ---
colorscale = [
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

# --- Layout réutilisable ---
def layout():
    return html.Div(
        className="world_data_container",
        children=[
            html.H3(
                "Research women in science",
                style={
                    "font-size": "24px",
                    "font-weight": "600",
                    "color": "#410919",
                    "margin-bottom": "15px",
                    "letter-spacing": "0.5px"
                },
            ),
            dcc.Dropdown(
                id="fr_phd_year",
                options=[{"label": y, "value": y} for y in years],
                value="2020-2021",
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
            dcc.Graph(
                id="fr_phd_histogram",
                config={
                    "displayModeBar": False,
                    "responsive": True
                }
            ),
        ]
    )

# --- Callback ---
@callback(
    Output("fr_phd_histogram", "figure"),
    Input("fr_phd_year", "value")
)
def update_fr_random_histogram(selected_year):
    fig = px.bar(
        df,
        y="discipline",
        x=selected_year,
        color=selected_year,
        color_continuous_scale=colorscale,
        range_color=(0, 100),
        labels={
            "discipline": "Sciences",
            selected_year: "Women (%)"
        },
        hover_data=["discipline"]
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        height=600,
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        font=dict(family="SF Pro Display"),
    )
    fig.update_yaxes(showgrid=True, gridcolor="#DDDDDD")

    return fig
