import json
import pandas as pd
import geopandas as gpd
import plotly.express as px
from dash import html, dcc, callback
from dash.dependencies import Input, Output
from src.charts.slider import create_slider
from src.components.segmented_control import create_segmented_control
from config import COLORSCALE_PINK

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

merged_df["GII_hover"] = merged_df["GII"].where(
    merged_df["GII"].notna(),
    "Unknown"
)

merged_df["Country_hover"] = merged_df["Country"]

iso3_to_name = {
    feature["properties"]["iso3"]: feature["properties"]["name"]
    for feature in world_geojson["features"]
}

merged_df["Country_hover"] = merged_df.apply(
    lambda row: iso3_to_name.get(row["plot_iso"])
    if pd.isna(row["Country_hover"])
    else row["Country_hover"],
    axis=1
)

zmin = merged_df["GII_plot"].min()
zmax = merged_df["GII_plot"].max()

def create_choropleth(df_year):
    fig = px.choropleth(
        df_year,
        geojson=world_geojson,
        locations="plot_iso",
        color="GII_plot",
        hover_name="Country_hover",
        hover_data=["ISO3", "GII_hover"],
        featureidkey="properties.iso3",
        projection="natural earth",
        color_continuous_scale=COLORSCALE_PINK,
        range_color=(zmin, zmax)
    )
    fig.update_traces(
        marker_line_color="#DDDDDD", 
        marker_line_width=0.9, 
        hovertemplate=
            "<b>%{hovertext}</b><br>"
            "ISO3: %{customdata[0]}<br>"
            "GII: %{customdata[1]}<extra></extra>"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), coloraxis_colorbar=dict(title="GII"))
    return fig

figs_by_year = {y: create_choropleth(merged_df[merged_df["Year"] == y]) for y in years}

def layout():
    return html.Div(
        className="data_container",
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
            create_slider(years, slider_id="gii"),
        ]
    )

@callback(
    Output("gii_map", "figure"),
    Input({"type": "year-slider", "id": "gii"}, "value"),
    Input("earth_selector", "value"),
)
def update_map_and_projection(year_selected, earth_selected):
    fig = figs_by_year[year_selected]

    if earth_selected == "Plan":
        fig.update_geos(projection_type="natural earth")
    else:
        fig.update_geos(projection_type="orthographic")

    return fig