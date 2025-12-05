from dash import html
from src.components.card import create_card

def layout():
    return html.Div(
        className="home-page",
        children=[
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
        ]
    )