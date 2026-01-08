import json
import pandas as pd
import geopandas as gpd
import plotly.express as px
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from src.charts.gii_slider import create_gii_slider
from src.components.segmented_control import create_segmented_control

df = pd.read_csv("data/raw/world_GII.csv")
world = gpd.read_file("data/cleaned/world_boundaries_simplified.geojson")

with open("data/cleaned/world_boundaries_simplified.geojson") as f:
    world_geojson = json.load(f)

gii_columns = [col for col in df.columns if col.startswith("Gender Inequality Index")]

df_long = df.melt(
    id_vars=["ISO3", "Country", "Continent"],
    value_vars=gii_columns,
    var_name="Year",
    value_name="GII"
)

df_long["Year"] = df_long["Year"].str.extract(r"(\d{4})").astype(int)
years = sorted(df_long["Year"].unique())

all_countries = world[['iso3']].copy()
all_years = pd.DataFrame({'Year': years})
all_combinations = all_countries.merge(all_years, how='cross')

merged_df = all_combinations.merge(
    df_long,
    left_on=['iso3', 'Year'],
    right_on=['ISO3', 'Year'],
    how='left'
)

merged_df['ISO3'] = merged_df['ISO3'].fillna(merged_df['iso3'])
merged_df['plot_iso'] = merged_df['ISO3']

real_min = df_long["GII"].min(skipna=True)
sentinel = real_min - (abs(real_min) * 0.1 + 0.01)

merged_df["GII_plot"] = merged_df["GII"].fillna(sentinel)

colorscale = [
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

zmin = merged_df["GII_plot"].min()
zmax = merged_df["GII_plot"].max()

def create_choropleth(df_year):
    fig = px.choropleth(
        df_year,
        geojson=world_geojson,
        locations="plot_iso",
        color="GII_plot",
        hover_name="Country",
        featureidkey="properties.iso3",
        projection="natural earth",
        color_continuous_scale=colorscale,
        range_color=(zmin, zmax)
    )
    fig.update_traces(marker_line_color="#DDDDDD", marker_line_width=0.9)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), coloraxis_colorbar=dict(title="GII"))
    return fig

figs_by_year = {y: create_choropleth(merged_df[merged_df["Year"] == y]) for y in years}

def layout():
    return html.Div(
        className="gii_data_container",
        children=[
            create_segmented_control(
                className="segmented_control small middle",
                id="earth_selector",
                options=["Plan", "Globe"]
            ),
            dcc.Graph(
                id="gii_map",
                figure=figs_by_year[years[0]],
                config={"displayModeBar": False, "responsive": True},
            ),
            create_gii_slider(years, "gii_slider"),
        ]
    )

@callback(
    Output("gii_map", "figure"),
    Input("gii_slider", "value"),
    Input("earth_selector", "value")
)
def update_map_and_projection(year_selected, earth_selected):
    fig = figs_by_year[year_selected]
    if earth_selected == "Plan":
        fig.update_geos(projection_type="natural earth")
    else:
        fig.update_geos(projection_type="orthographic")

    return fig