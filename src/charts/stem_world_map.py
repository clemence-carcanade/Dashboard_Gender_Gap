from dash import html, dcc, callback
from dash.dependencies import Input, Output
from src.components.segmented_control import create_segmented_control
from src.charts.slider import create_slider
from config import COLORSCALE_BLUE
from src.utils.prepare_data import get_stem_data, get_stem_filtered_years, get_world_geojson, prepare_world_choropleth_data
from src.utils.chart import create_world_choropleth, update_projection

VALUE_COL = ("Female share of graduates from Science, Technology, Engineering and Mathematics (STEM) programmes, tertiary (%)")

df = get_stem_data()
years = get_stem_filtered_years()
geojson = get_world_geojson()

merged_df, sentinel = prepare_world_choropleth_data(
    df=df,
    value_col=VALUE_COL,
    years=years,
    iso_col='Code',
    entity_col='Entity'
)

zmin = sentinel
zmax = merged_df[f"{VALUE_COL}_plot"].max()

def create_stem_choropleth(df_year):
    return create_world_choropleth(
        df=df_year,
        geojson=geojson,
        locations_col="plot_iso",
        color_col=f"{VALUE_COL}_plot",
        hover_name_col="Country_hover",
        hover_data_cols=["plot_iso", f"{VALUE_COL}_hover"],
        featureidkey="properties.iso3",
        colorscale=COLORSCALE_BLUE,
        range_color=(zmin, zmax),
        colorbar_title="Women in<br>STEM (%)",
        hover_template=(
            "<b>%{hovertext}</b><br>"
            "ISO3: %{customdata[0]}<br>"
            "STEM (%): %{customdata[1]}<extra></extra>"
        ),
        projection="natural earth",
    )

figs_by_year = {
    y: create_stem_choropleth(merged_df[merged_df["Year"] == y])
    for y in years
}

def layout():
    return html.Div(
        className="data_container",
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
    
    projection_type = "natural earth" if earth_selected == "Plan" else "orthographic"
    update_projection(fig, projection_type)
    
    return fig