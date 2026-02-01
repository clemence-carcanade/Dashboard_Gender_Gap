from dash import html, dcc, callback
from dash.dependencies import Input, Output
from src.charts.slider import create_slider
from src.components.segmented_control import create_segmented_control
from config import COLORSCALE_PINK
from src.utils.prepare_data import get_gii_long_format, get_world_geojson, prepare_world_choropleth_data
from src.utils.chart import create_world_choropleth, update_projection

df_long = get_gii_long_format()
geojson = get_world_geojson()
years = sorted(df_long["Year"].unique())

merged_df, sentinel = prepare_world_choropleth_data(
    df=df_long,
    value_col="GII",
    years=years,
    iso_col='ISO3',
    entity_col='Country'
)

zmin = merged_df["GII_plot"].min()
zmax = merged_df["GII_plot"].max()

def create_gii_choropleth(df_year):
    return create_world_choropleth(
        df=df_year,
        geojson=geojson,
        locations_col="plot_iso",
        color_col="GII_plot",
        hover_name_col="Country_hover",
        hover_data_cols=["ISO3", "GII_hover"],
        featureidkey="properties.iso3",
        colorscale=COLORSCALE_PINK,
        range_color=(zmin, zmax),
        colorbar_title="GII",
        hover_template=(
            "<b>%{hovertext}</b><br>"
            "ISO3: %{customdata[0]}<br>"
            "GII: %{customdata[1]}<extra></extra>"
        ),
        projection="natural earth",
    )

figs_by_year = {
    y: create_gii_choropleth(merged_df[merged_df["Year"] == y])
    for y in years
}


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
    
    projection_type = "natural earth" if earth_selected == "Plan" else "orthographic"
    update_projection(fig, projection_type)
    
    return fig