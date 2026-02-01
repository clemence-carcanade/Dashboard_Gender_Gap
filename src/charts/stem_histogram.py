from dash import Input, Output, html, dcc, callback
from src.charts.slider import create_slider
from config import COLORSCALE_BLUE
from src.utils.get_data import get_stem_data, get_stem_filtered_years
from src.utils.chart import create_bar_chart

VALUE_COL = ("Female share of graduates from Science, Technology, Engineering and Mathematics (STEM) programmes, tertiary (%)")

df = get_stem_data()
years = get_stem_filtered_years()

zmin = df[VALUE_COL].min()
zmax = df[VALUE_COL].max()

def layout():
    return html.Div(
        className="data_container",
        children=[
            dcc.Graph(
                id="stem_histogram",
                config={"displayModeBar": False, "responsive": True}
            ),
            create_slider(years, slider_id="stem"),
        ]
    )

@callback(
    Output("stem_histogram", "figure"),
    Input({"type": "year-slider", "id": "stem"}, "value")
)
def update_stem_histogram(selected_year):
    df_filtered = df[df["Year"] == selected_year].copy()
    df_filtered["Country_short"] = df_filtered["Entity"].str.slice(0, 8)
    
    fig = create_bar_chart(
        df=df_filtered,
        x='Country_short',
        y=VALUE_COL,
        color_col=VALUE_COL,
        colorscale=COLORSCALE_BLUE,
        labels={
            VALUE_COL: "Women in<br>STEM (%)",
            "Country_short": "Countries",
        },
        hover_template="<b>%{customdata[0]}</b><br>STEM (%): %{y}<extra></extra>",
        range_color=(zmin, zmax),
        custom_data=['Entity'],
        xaxis_angle=-45,
    )
    
    fig.update_layout(yaxis=dict(range=[0, zmax]))
    
    return fig