import plotly.express as px
from dash import html, dcc
import pandas as pd

df = pd.read_csv("data/cleaned/fr_regions_gender_inequality_cleaned.csv")

REGION_NAMES = ['Île-de-France', 'Centre-Val de Loire', 'Bourgogne-Franche-Comté', 
                'Normandie', 'Hauts-de-France', 'Grand Est', 'Pays de la Loire', 
                'Bretagne', 'Nouvelle-Aquitaine', 'Occitanie', 'Auvergne-Rhône-Alpes',
                'Provence-Alpes-Côte d\'Azur', 'Corse', 'France métropolitaine hors Ile-de-France',
                'France métropolitaine', 'Guadeloupe', 'Martinique', 'Guyane', 'La Réunion',
                'DROM hors Mayotte', 'France hors Mayotte']

df_departments = df[~df['Region'].isin(REGION_NAMES)].copy()
df_departments = df_departments.dropna(subset=['Education_Gap_2021'])

df_departments['Salary_Gap_2022_abs'] = df_departments['Salary_Gap_2022'].abs()

bins = [0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5]
labels = ['0-2.5%', '2.5-5%', '5-7.5%', '7.5-10%', '10-12.5%', '12.5-15%', '15-17.5%', '17.5-20%', '20-22.5%']

df_departments['Education_Gap_Range'] = pd.cut(
    df_departments['Education_Gap_2021'],
    bins=bins,
    labels=labels,
    include_lowest=True
)

df_departments['Salary_Gap_Range'] = pd.cut(
    df_departments['Salary_Gap_2022_abs'],
    bins=bins,
    labels=labels,
    include_lowest=True
)

colorscale_pink = [
    [0.0, "#F4C3E0"],
    [0.2, "#EDA1CE"],
    [0.4, "#E576B8"],
    [0.6, "#DE4FA5"],
    [0.8, "#D62991"],
    [1.0, "#B02177"],
]

colorscale_blue = [
    [0.0, "#9BBDEE"],
    [0.2, "#73A4E7"],
    [0.4, "#2570DA"],
    [0.6, "#1E5CB3"],
    [0.8, "#18488C"],
    [1.0, "#113464"],
]

def education_bars_layout(metric):
    fig = create_bar_figure(metric)

    return html.Div(
        className="world_data_container",
        children=[
            dcc.Graph(
                figure=fig,
                config={"displayModeBar": False, "responsive": True}
            )
        ]
    )

def create_bar_figure(selected_metric):

    if selected_metric == "Disparity in Education":
        counts = (
            df_departments
            .groupby('Education_Gap_Range', observed=False)
            .size()
            .reset_index(name='count')
        )

        fig = px.bar(
            counts,
            x='Education_Gap_Range',
            y='count',
            labels={
                'Education_Gap_Range': "Women exceeding Men in Higher Education (%)",
                'count': "Nombre de départements"
            },
            color='count',
            color_continuous_scale=colorscale_pink
        )

        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Départements: %{y}<extra></extra>'
        )

        fig.update_layout(yaxis_title="Departments number")

    else:  # Wage Inequality
        counts = (
            df_departments
            .groupby('Salary_Gap_Range', observed=False)
            .size()
            .reset_index(name='count')
        )

        fig = px.bar(
            counts,
            x='Salary_Gap_Range',
            y='count',
            labels={
                'Salary_Gap_Range': "Difference in Wage between Women and Men (%)",
                'count': "Nombre de départements"
            },
            color='count',
            color_continuous_scale=colorscale_blue
        )

        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Departments: %{y}<extra></extra>'
        )

        fig.update_layout(yaxis_title="Departments number")

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="SF Pro Display"),
        showlegend=False,
        coloraxis_showscale=False,
    )

    fig.update_yaxes(showgrid=True, gridcolor="#DDDDDD")
    fig.update_xaxes(showgrid=False)

    return fig