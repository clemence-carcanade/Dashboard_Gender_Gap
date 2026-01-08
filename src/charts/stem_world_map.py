import json
import pandas as pd
import geopandas as gpd
import plotly.express as px
from dash import html, dcc, callback
from dash.dependencies import Input, Output
from src.components.segmented_control import create_segmented_control
from src.charts.slider import create_slider

df = pd.read_csv("data/raw/world_women_in_stem.csv")
world = gpd.read_file("data/cleaned/world_boundaries_simplified.geojson")

with open("data/cleaned/world_boundaries_simplified.geojson") as f:
    world_geojson = json.load(f)

VALUE_COL = (
    "Female share of graduates from Science, Technology, Engineering and Mathematics (STEM) programmes, tertiary (%)"
)

df = df.dropna(subset=[VALUE_COL])
df["Year"] = df["Year"].astype(int)

years = sorted(y for y in df["Year"].unique() if y not in (1998, 2019))

all_countries = world[['iso3']].copy()
all_years = pd.DataFrame({'Year': years})
all_combinations = all_countries.merge(all_years, how='cross')

merged_df = all_combinations.merge(
    df,
    left_on=['iso3', 'Year'],
    right_on=['Code', 'Year'],
    how='left'
)

merged_df['Code'] = merged_df['Code'].fillna(merged_df['iso3'])
merged_df['plot_iso'] = merged_df['Code']

real_min = df[VALUE_COL].min()
sentinel = real_min - (abs(real_min) * 0.1 + 0.01)

merged_df["STEM_plot"] = merged_df[VALUE_COL].fillna(sentinel)

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

zmin = sentinel
zmax = merged_df["STEM_plot"].max()

def create_choropleth(df_year):
    fig = px.choropleth(
        df_year,
        geojson=world_geojson,
        locations="plot_iso",
        color="STEM_plot",
        hover_name="Entity",
        featureidkey="properties.iso3",
        projection="natural earth",
        color_continuous_scale=colorscale,
        range_color=(zmin, zmax),
    )

    fig.update_traces(marker_line_color="#DDDDDD", marker_line_width=0.9)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(title="Women in STEM (%)"),
    )
    return fig

figs_by_year = {
    y: create_choropleth(merged_df[merged_df["Year"] == y])
    for y in years
}

def layout():
    return html.Div(
        className="stem_data_container",
        children=[
            create_segmented_control(
                className="segmented_control small middle",
                id="earth_selector_stem",
                options=["Plan", "Globe"],
            ),
            dcc.Graph(
                id="stem_map",
                figure=figs_by_year[years[0]],
                config={"displayModeBar": False, "responsive": True},
            ),
            create_slider(years, slider_id="stem"),
        ],
    )

@callback(
    Output("stem_map", "figure"),
    Input({"type": "year-slider", "id": "stem"}, "value"),
    Input("earth_selector_stem", "value"),
)
def update_stem_map(year_selected, earth_selected):
    fig = figs_by_year[year_selected]

    fig.update_geos(
        projection_type="natural earth"
        if earth_selected == "Plan"
        else "orthographic"
    )

    return fig