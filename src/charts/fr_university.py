# IMPORTS
import plotly.express as px
from dash import html, dcc, Input, Output, callback
import pandas as pd
import csv
from src.components.segmented_control import create_segmented_control

discipline_translation = {
    "Universités - Formations scientifiques y compris ingénieurs": "Engineering",
    "Sciences fondamentales et applications": "Fundamental",
    "Sciences de la Vie, de la santé, de la Terre et de l'Univers": "Life, Health & Earth",
    "Plurisciences1": "Multidisciplinary",
    "Universités - Santé": "Health",
    "Médecine et odontologie": "Medicine & Dentistry",
    "Pharmacie": "Pharmacy",
    "Plurisanté (Paces et Pass2)": "Multidisciplinary Health",
    "DUT - Spécialités de la production et de l'informatique": "DUT - Production & IT",
    "Ensemble": "All Bachelor"
}

with open(
    "data/raw/fr_research_women_feuille1.csv",
    newline="",
    encoding="utf-8"
) as fichier:
    lecteur = csv.reader(fichier)
    lignes = list(lecteur)

for i, ligne in enumerate(lignes):
    if "2010-2011" in ligne and "2020-2021" in ligne:
        index_header = i
        break

col_discipline = 0
col_2010 = lignes[index_header].index("2010-2011")
col_2020 = lignes[index_header].index("2020-2021")

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
df["discipline"] = df["discipline"].str.strip().replace(discipline_translation)

years = ["2010-2011", "2020-2021"]

colorscale = [
    [0.0, "#EDEDED"],
    [0.1, "#F4C3E0"],
    [0.2, "#EDA1CE"],
    [0.3, "#E576B8"],
    [0.4, "#DE4FA5"],
    [0.6, "#D62991"],
    [0.8, "#B02177"],
    [0.9, "#891A5D"],
    [1.0, "#631343"],
]

def layout():
    return html.Div(
        className="world_data_container",
        children=[
            create_segmented_control(
                className="segmented_control small middle",
                id="fr_university_year",
                options=years,
            ),
            dcc.Graph(
                id="fr_university_histogram",
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            ),
            html.A(
                "INSEE",
                href="https://www.insee.fr/fr/statistiques/6047727?sommaire=6047805#",
                target="_blank",
                className="source study",
            ),
        ],
    )

@callback(
    Output("fr_university_histogram", "figure"),
    Input("fr_university_year", "value"),
)
def update_fr_university_histogram(selected_year):
    fig = px.bar(
        df,
        y="discipline",
        x=selected_year,
        color=selected_year,
        color_continuous_scale=colorscale,
        range_color=(0, 100),
        labels={
            "discipline": "Sciences",
            selected_year: "Women (%)",
        },
        hover_data=["discipline"],
    )

    fig.update_layout(
        xaxis_title="Women's Share in Higher Education in Science (%)",
        xaxis=dict(range=[0, 100]),
        xaxis_tickangle=-45,
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        font=dict(family="SF Pro Display", size=14),
    )

    fig.update_yaxes(title=None, showgrid=True, gridcolor="#DDDDDD")
    fig.update_xaxes(showgrid=True, gridcolor="#DDDDDD")
    fig.update_layout(coloraxis_showscale=False)

    return fig