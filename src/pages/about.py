from dash import html
from src.components.card import create_card


def layout():
    return html.Div(
        className="about-page",
        children=[
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--pink)",
                    "--top": "90px",
                    "--right": "450px"
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
                    "--top": "50px",
                    "--right": "-20px"
                }
            ),
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--pink)",
                    "--top": "350px",
                    "--right": "-20px"
                }
            ),
            # Gros conteneur de texte
            html.Div(
                className="content-row",
                children=[
                        html.Img(
                        src="/assets/images/Clems_Logo.png",
                        className="logo-image",
                        alt="clem_logo"
                    ),
                        html.Div(
                            className="main-text-container",
                            children=[
                                html.H1("About us..."),
                                html.P("This Dashboard was created as part of an academic project for the ESIEE Paris engineering school in the Computer Science and Applications apprenticeship program, by Clémence Carcanade, apprentice at Dassault Système, and Thaïs Castillo, apprentice at Crédit Agricole Payment Services.")
                            ]
                        ),
                        # Petits conteneurs alignés en dessous
                ]
            ),
            html.Div(
                            className="cards-row",
                            children=[
                                create_card(
                                    html.Div(
                                        className="titre-card",
                                        children=[
                                            html.H3("Project goals :"),
                                            html.Br(),
                                            "This dashboard highlights a major societal issue: the link between global innovation and the inclusion of women. We first analyze the Global Innovation Index (GII), before examining the proportion of women in STEM fields internationally. Finally, we take a specific look at France, examining disparities in higher education and wage gaps.",
                                            html.Br(),
                                        ]
                                    )
                                ),
                                create_card(
    html.Div(
        className="titre-card",
        children=[
            html.H3("Tools used"),
            html.Div(
                className="card-lines",
                children=[
                    html.Div(
                        className="card-line",
                        children=[
                            html.Img(
                                src="/assets/images/python.png",
                                className="card-icon"
                            ),
                            html.Span("Python 3.12")
                        ]
                    ),
                    html.Div(
                        className="card-line",
                        children=[
                            html.Img(
                                src="/assets/images/pandas_white.png",
                                className="card-icon"
                            ),
                            html.Span("Pandas")
                        ]
                    ),
                    html.Div(
                        className="card-line",
                        children=[
                            html.Img(
                                src="/assets/images/css.png",
                                className="card-icon"
                            ),
                            html.Span("CSS")
                        ]
                    ),
                    html.Div(
                        className="card-line",
                        children=[
                            html.Img(
                                src="/assets/images/plotly.webp",
                                className="card-icon"
                            ),
                            html.Span("Plotly, Dash")
                        ]
                    ),
                ]
            ),
        ]
    )
)
,
                            ]
                        )   
        ]
    )