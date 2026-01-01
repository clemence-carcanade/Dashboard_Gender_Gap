import json
import pandas as pd
import geopandas as gpd
import plotly.express as px
import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State

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

merged_df = world.merge(
    df_long,
    left_on="iso3",
    right_on="ISO3",
    how="outer"
)
merged_df["plot_iso"] = merged_df["ISO3"].fillna(merged_df["iso3"])

real_min = df_long["GII"].min(skipna=True)
sentinel = real_min - (abs(real_min) * 0.1 + 0.01)
merged_df["GII_plot"] = merged_df["GII"].fillna(sentinel)

colorscale = [
    [0.0, "#F5F5F5"],
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
    fig.update_traces(marker_line_color="#EDEDED", marker_line_width=0.9)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), coloraxis_colorbar=dict(title="GII"))
    return fig

fig = create_choropleth(merged_df[merged_df["Year"] == years[0]])
figs_by_year = {y: create_choropleth(merged_df[merged_df["Year"] == y]) for y in years}

def layout():
    return html.Div(
        className="gii_map_container",
        children=[
            dcc.Graph(
                id="gii_map",
                figure=fig,
                config={"displayModeBar": False},
            ),
            html.Div(
                className="slider",
                children=[
                    dcc.Slider(
                        id="gii_slider",
                        min=int(years[0]),
                        max=int(years[-1]),
                        step=1,
                        value=int(years[-1]),
                        marks={int(y): str(y) for y in years},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    html.Button("▶", id="play_pause_button", n_clicks=0),
                    dcc.Interval(
                        id="interval",
                        interval=500,
                        n_intervals=0,
                        disabled=False
                    )
                ]
            )
        ]
    )

@callback(
    Output("interval", "disabled"),
    Output("play_pause_button", "children"),
    Input("play_pause_button", "n_clicks"),
    State("interval", "disabled")
)
def toggle_play_pause(n_clicks, disabled):
    if n_clicks is None:
        return True, "▶"
    new_disabled = not disabled
    new_label = "⏸" if not new_disabled else "▶"
    return new_disabled, new_label

@callback(
    Output("gii_map", "figure"),
    Input("gii_slider", "value")
)
def update_map(year_selected):
    return figs_by_year[year_selected]

@callback(
    Output("gii_slider", "value"),
    Input("interval", "n_intervals"),
    State("gii_slider", "value")
)
def update_slider(n_intervals, current_year):
    idx = years.index(current_year)
    if idx + 1 >= len(years):
        return years[0]
    return years[idx + 1]