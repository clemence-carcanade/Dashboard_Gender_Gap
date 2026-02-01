from dash import html, dcc, Input, Output, callback
from src.components.segmented_control import create_segmented_control
from config import COLORSCALE_BLUE
from src.utils.get_data import get_fr_phd_data
from src.utils.chart import create_bar_chart

df = get_fr_phd_data()
years = ["2010-2011", "2020-2021"]

def layout():
    return html.Div(
        className="data_container",
        children=[
            create_segmented_control(
                className="segmented_control small middle",
                id="fr_phd_year",
                options=years,
            ),
            dcc.Graph(
                id="fr_phd_histogram",
                config={"displayModeBar": False, "responsive": True}
            ),
            html.A(
                "INSEE",
                href="https://www.insee.fr/fr/statistiques/6047727?sommaire=6047805#",
                target="_blank",
                className="source study",
            ),
        ]
    )

@callback(
    Output("fr_phd_histogram", "figure"),
    Input("fr_phd_year", "value")
)
def update_fr_phd_histogram(selected_year):
    fig = create_bar_chart(
        df=df,
        x=selected_year,
        y="discipline",
        color_col=selected_year,
        colorscale=COLORSCALE_BLUE,
        labels={
            "discipline": "Sciences",
            selected_year: "Women (%)"
        },
        hover_template="<b>%{customdata[0]}</b><br>Women (%): %{customdata[1]:.1f}<extra></extra>",
        xaxis_title="Women's Share among PhD Students in Science (%)",
        height=525,
        range_color=(0, 100),
        custom_data=["discipline", selected_year],
        xaxis_angle=-45,
    )

    fig.update_layout(xaxis=dict(range=[0, 100]))
    fig.update_yaxes(title=None)
    
    return fig