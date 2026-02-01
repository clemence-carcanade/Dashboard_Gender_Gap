from dash import html, dcc, Input, Output, callback
from src.components.segmented_control import create_segmented_control
from config import COLORSCALE_PINK
from src.utils.prepare_data import get_fr_university_data
from src.utils.chart import create_bar_chart

df = get_fr_university_data()
years = ["2010-2011", "2020-2021"]

def layout():
    return html.Div(
        className="data_container",
        children=[
            create_segmented_control(
                className="segmented_control small middle",
                id="fr_university_year",
                options=years,
            ),
            dcc.Graph(
                id="fr_university_histogram",
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            ),
            html.A(
                "INSEE",
                href="https://www.insee.fr/fr/statistiques/6047727?sommaire=6047805#",
                target="_blank",
                className="source study",
            ),
        ],
    )

@callback(
    Output("fr_university_histogram", "figure"),
    Input("fr_university_year", "value"),
)
def update_fr_university_histogram(selected_year):
    fig = create_bar_chart(
        df=df,
        x=selected_year,
        y="discipline",
        color_col=selected_year,
        colorscale=COLORSCALE_PINK,
        labels={
            "discipline": "Sciences",
            selected_year: "Women (%)",
        },
        hover_template="<b>%{customdata[0]}</b><br>Women (%): %{customdata[1]:.1f}<extra></extra>",
        xaxis_title="Women's Share in Higher Education in Science (%)",
        range_color=(0, 100),
        custom_data=["discipline", selected_year],
    )

    fig.update_layout(xaxis=dict(range=[0, 100]))
    fig.update_yaxes(title=None)
    
    return fig