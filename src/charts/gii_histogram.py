from dash import Input, Output, html, dcc, callback
from src.charts.slider import create_slider
from src.components.segmented_control import create_segmented_control
from config import COLORSCALE_PINK
from src.utils.get_data import get_gii_long_format
from src.utils.chart import create_bar_chart

df_long = get_gii_long_format()
years = sorted(df_long["Year"].unique())
continents = ["All"] + sorted(df_long["Continent"].dropna().unique())

zmin = df_long["GII"].min()
zmax = df_long["GII"].max()

def layout():
    return html.Div(
        className="data_container",
        children=[
            create_segmented_control(
                className="segmented_control small middle",
                id="continent_selector",
                options=continents,
            ),
            dcc.Graph(
                id='gii_histogram',
                config={"displayModeBar": False, "responsive": True}
            ),
            create_slider(years, slider_id="gii"),
        ]
    )


@callback(
    Output('gii_histogram', 'figure'),
    [Input({"type": "year-slider", "id": "gii"}, "value"),
     Input('continent_selector', 'value')]
)
def update_histogram(selected_year, selected_continent):
    df_filtered = df_long[df_long["Year"] == selected_year].copy()

    if selected_continent != "All":
        df_filtered = df_filtered[df_filtered["Continent"] == selected_continent]
        df_filtered["Country_short"] = df_filtered["Country"].str.slice(0, 8)
        x_col = 'Country_short'
        show_xlabels = True
        x_title = None
    else:
        x_col = 'Country'
        show_xlabels = False
        x_title = "Countries"
    
    fig = create_bar_chart(
        df=df_filtered,
        x=x_col,
        y='GII',
        color_col='GII',
        colorscale=COLORSCALE_PINK,
        labels={'GII': 'GII', x_col: 'Countries'},
        hover_template='<b>%{customdata[0]}</b><br>GII: %{y}<extra></extra>',
        range_color=(zmin, zmax),
        custom_data=['Country'],
        xaxis_angle=-45,
    )
    
    fig.update_layout(
        yaxis=dict(range=[0, zmax]),
        coloraxis_colorbar=dict(len=1.5),
    )
    
    fig.update_xaxes(
        showticklabels=show_xlabels,
        title=x_title
    )
    
    return fig