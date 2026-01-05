from dash import html
from src.components.card import create_card
from src.components.segmented_control import create_segmented_control
from src.charts.gii_world_map import layout as gii_map_layout
from src.charts.gii_board import layout as gii_board_layout
from src.charts.gii_histogram import layout as gii_bar_layout

def layout():
    return html.Div(
        className="home-page",
        children=[
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--pink)",
                    "--top": "60px",
                    "--right": "550px"
                }
            ),
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--pink)",
                    "--top": "350px",
                    "--left": "50px"
                }
            ),
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--blue)",
                    "--top": "500px",
                    "--right": "450px"
                }
            ),
            html.Div(
                className="title",
                children=[
                    create_card(
                        html.H1("\"Where are the women in science?\""),
                        html.H3("This question, still asked far too often, highlights the persistent gender inequalities in scientific fields."),
                        html.P("As part of a student project focused on creating an interactive dashboard in Python, we chose to explore these inequalities in depth. The aim of this work is to shed light on the disparities between women and men in science, both in France and worldwide, using reliable data and recognized studies. We selected this topic because it resonates strongly with us: as women studying in digital and engineering fields, we are directly concerned by the underrepresentation of women in these domains, which remain largely male-dominated. This project is therefore both an analytical exercise and a personal commitment, intended to raise awareness and inform through educational data visualizations.")
                    ),
                    html.Img(
                        src="/assets/images/gender_balance.png",
                        className="gender-image",
                        alt="gender_equality_balance"
                    )
                ]
            ),
            html.Div(
                className="quote",
                children=[
                    create_card(
                        html.Img(
                            src="/assets/images/undp.jpg",
                            className="undp-logo",
                            alt="undp_logo"
                        ),
                        html.H3(
                            className="h3_normal",
                            children=[
                                "“",
                                html.I(
                                    "GII is a composite metric of gender inequality using three dimensions: reproductive health, empowerment and the labour market. "
                                    "A low GII value indicates low inequality between women and men, and vice-versa."
                                ),
                                "” UNDP"
                            ]
                        )
                    ),
                ]
            ),
            create_segmented_control(
                options=["Gender Inequality Index", "Women's Share in Research"],
                className="segmented_control",
                id="data_selector"
            ),
            html.Div(
                className="world_analysis",
                children=[
                    create_segmented_control(
                        options=["🌍 Map", "📊 Bars"],
                        className="segmented_control small",
                        id="view_selector"
                    ),
                    html.Div(
                        className="gii_container",
                        id="gii_container",
                        children=[
                            gii_map_layout(),
                            gii_board_layout(),
                        ]
                    ),
                ]
            )
        ]
    )