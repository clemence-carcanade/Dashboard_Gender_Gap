# IMPORTS
import plotly.express as px
from dash import html, dcc, Input, Output, callback
import pandas as pd
import csv

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
years = ["2010-2011", "2020-2021"]

colorscale = [
    [0.0, "#EDEDED"],
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
        className="world_data_container",
        children=[
            html.H3(
                "Research women in science",
                style={
                    "font-size": "24px",
                    "font-weight": "600",
                    "color": "#410919",
                },
            ),
            dcc.Dropdown(
                id="fr_research_year",
                options=[{"label": y, "value": y} for y in years],
                value="2020-2021",
                clearable=False,
                searchable=False,
            ),
            dcc.Graph(
                id="fr_research_histogram",
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            ),
        ],
    )

@callback(
    Output("fr_research_histogram", "figure"),
    Input("fr_research_year", "value"),
)
def update_fr_research_histogram(selected_year):
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
        xaxis_tickangle=-45,
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        font=dict(family="SF Pro Display"),
    )

    fig.update_yaxes(showgrid=True, gridcolor="#DDDDDD")

    return fig