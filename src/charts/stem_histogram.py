import plotly.express as px
from dash import Input, Output, html, dcc, callback
import pandas as pd
from src.charts.slider import create_slider

df = pd.read_csv("data/raw/world_women_in_stem.csv")

VALUE_COL = (
    "Female share of graduates from Science, Technology, Engineering and Mathematics (STEM) programmes, tertiary (%)"
)

years = sorted(
    y for y in df["Year"].unique()
    if y not in (1998, 2019)
)

colorscale = [
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

zmin = df[VALUE_COL].min()
zmax = df[VALUE_COL].max()

def layout():
    return html.Div(
        className="world_data_container",
        children=[
            dcc.Graph(
                id="stem_histogram",
                config={
                    "displayModeBar": False,
                    "responsive": True
                }
            ),
            create_slider(years, slider_id="stem"),
        ]
    )

@callback(
    Output("stem_histogram", "figure"),
    Input({"type": "year-slider", "id": "stem"}, "value")
)
def update_stem_histogram(selected_year):
    df_filtre = df[df["Year"] == selected_year]
    df_filtre["Country_short"] = df_filtre["Entity"].str.slice(0, 8)
    x_col = 'Country_short'

    fig = px.bar(
        df_filtre,
        x=x_col,
        y=VALUE_COL,
        color=VALUE_COL,
        color_continuous_scale=colorscale,
        labels={
            VALUE_COL: "Women in<br>STEM (%)",
            "Entity": "Countries",
            "Country_short": "Countries",
        },
        hover_data={
            "Entity": True,
            VALUE_COL: True,
        },
        range_color=(zmin, zmax),
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        yaxis=dict(range=[0, zmax]),
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        font=dict(family="SF Pro Display"),
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#DDDDDD",
    )

    return fig