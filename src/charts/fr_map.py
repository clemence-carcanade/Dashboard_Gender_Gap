import json
import pandas as pd
import plotly.express as px
from dash import html, dcc

df = pd.read_csv("data/cleaned/fr_regions_gender_inequality_cleaned.csv")

REGION_NAMES = ['Île-de-France', 'Centre-Val de Loire', 'Bourgogne-Franche-Comté', 
                'Normandie', 'Hauts-de-France', 'Grand Est', 'Pays de la Loire', 
                'Bretagne', 'Nouvelle-Aquitaine', 'Occitanie', 'Auvergne-Rhône-Alpes',
                'Provence-Alpes-Côte d\'Azur', 'Corse', 'France métropolitaine hors Ile-de-France',
                'France métropolitaine', 'Guadeloupe', 'Martinique', 'Guyane', 'La Réunion',
                'DROM hors Mayotte', 'France hors Mayotte']

df_departments = df[~df['Region'].isin(REGION_NAMES)].copy()

df_departments['Salary_Gap_2022_abs'] = df_departments['Salary_Gap_2022'].abs()

# Charger le GeoJSON des départements français
with open("data/raw/fr_departments.geojson") as f:
    france_geojson = json.load(f)

# Préparer les données pour la visualisation
df_departments['Code'] = df_departments['Code'].str.zfill(2)  # Assurer le format 01, 02, etc.

df_departments["has_edu_data"] = df_departments["Education_Gap_2021"].notna()
df_departments["has_sal_data"] = df_departments["Salary_Gap_2022"].notna()

real_min_edu = df_departments["Education_Gap_2021"].min(skipna=True)
real_min_sal = df_departments["Salary_Gap_2022_abs"].min(skipna=True)

sentinel_edu = real_min_edu - (abs(real_min_edu) * 0.1 + 0.01)
sentinel_sal = real_min_sal - (abs(real_min_sal) * 0.1 + 0.01)

df_departments["Education_Gap_plot"] = df_departments["Education_Gap_2021"].fillna(sentinel_edu)
df_departments["Salary_Gap_plot"] = df_departments["Salary_Gap_2022_abs"].fillna(sentinel_sal)

# Calculer les valeurs min et max pour l'échelle de couleur
zmin = df_departments["Education_Gap_2021"].min()
zmax = df_departments["Education_Gap_2021"].max()

# Palette de couleurs - du rose pâle au fuchsia foncé
colorscale_pink = [
    [0.0, "#EDEDED"],
    [0.00001, "#FBEAF4"],
    [0.1, "#F4C3E0"],
    [0.2, "#EDA1CE"],
    [0.3, "#E576B8"],
    [0.4, "#DE4FA5"],
    [0.5, "#D62991"],
    [0.6, "#B02177"],
    [0.7, "#891A5D"],
    [1.0, "#631343"],
]

colorscale_blue = [
    [0.0, "#EDEDED"],
    [0.00001, "#E9F1FB"],
    [0.1, "#C2D7F5"],
    [0.2, "#9BBDEE"],
    [0.3, "#73A4E7"],
    [0.4, "#2570DA"],
    [0.5, "#1E5CB3"],
    [0.6, "#18488C"],
    [0.7, "#113464"],
    [1.0, "#0A1F3D"],
]

def create_choropleth(metric):
    if metric == "Disparity in Education":
        color_col = "Education_Gap_plot"
        subtitle_text = "Women exceeding Men in Higher Education (%)"
        colorscale = colorscale_pink
        z_min = df_departments[color_col].min()
        z_max = df_departments["Education_Gap_2021"].max()
        hover_template = '<b>%{customdata[0]}</b><br>Écart d\'éducation: %{z:.1f}%<extra></extra>'
        colorbar_title = "Gap in<br>Education (%)"
    else:
        color_col = "Salary_Gap_plot"
        subtitle_text = "Difference in Wage between Women and Men (%)"
        colorscale = colorscale_blue
        z_min = df_departments[color_col].min()
        z_max = df_departments["Salary_Gap_2022_abs"].max()
        hover_template = '<b>%{customdata[0]}</b><br>Écart salarial: %{z:.1f}%<extra></extra>'
        colorbar_title = "Gap in<br>Wage (%)"

    fig = px.choropleth(
        df_departments,
        geojson=france_geojson,
        locations="Code",
        color=color_col,
        featureidkey="properties.code",
        color_continuous_scale=colorscale,
        range_color=(z_min, z_max),
        custom_data=['Region']
    )

    fig.update_traces(
        marker_line_color="#DDDDDD",
        marker_line_width=0.9,
        hovertemplate=hover_template
    )

    fig.update_geos(fitbounds="locations", visible=False)

    # Ajouter texte sous la carte dans le graphique
    fig.update_layout(
        annotations=[
            dict(
                text=subtitle_text,
                x=0.55,           # centré horizontalement
                y=-0,          # sous la carte
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(family="SF Pro Display", size=18, color="#333333")
            )
        ],
        margin=dict(l=0, r=0, t=0, b=0),  # laisser un peu d'espace en bas
        coloraxis_colorbar=dict(
            title=colorbar_title,
            thickness=30,
            len=0.95,
            y=0.5,
            bgcolor="rgba(255,255,255,0.8)",
            tickfont=dict(family="SF Pro Display", size=11),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="SF Pro Display"),
        geo=dict(
            projection_type="mercator",
            center=dict(lat=46.5, lon=2.5),
            projection_scale=15
        )
    )

    return fig

def education_map_layout(metric):
    fig = create_choropleth(metric)

    return html.Div(
        className="world_data_container",
        children=[
            dcc.Graph(
                figure=fig,
                config={"displayModeBar": False, "responsive": True}
            )
        ]
    )