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
                    "--top": "60px",
                    "--right": "450px"
                }
            ),
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--pink)",
                    "--top": "500px",
                    "--right": "450px"
                }
            ),
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--blue)",
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
                                html.P("Ce Dashboard a été réalisé dans le cadre d'un projet académique pour l'école d'ingénieure ESIEE Paris dans la filière en apprentissage Informatique et Applications, "
                                "par Clémence Carcanade, apprentie chez Dassault Système et Thaïs Castillo, apprentie chez Crédit Agricole Payment Services.")
                            ]
                        ),
                        # Petits conteneurs alignés en dessous
                ]
            ),
            html.Div(
                            className="cards-row",
                            children=[
                                create_card(
                                    html.P([
                                        html.Strong("Objectifs du projet :"),
                                        html.Br(),
                                        "Texte normal ligne 1",
                                        html.Br(),
                                        "Texte normal ligne 2",
                                        html.Br(),
                                        "Texte normal ligne 3"
                                    ])
                                ),
                                create_card(
                                    html.P([
                                        html.Strong("Outils utilisés :"),
                                        html.Br(),
                                        "Texte normal ligne 1",
                                        html.Br(),
                                        "Texte normal ligne 2",
                                        html.Br(),
                                        "Texte normal ligne 3"
                                    ])
                                ),
                                create_card(
                                    html.P([
                                        html.Strong("Pourquoi ce sujet ?"),
                                        html.Br(),
                                        "Texte normal ligne 1",
                                        html.Br(),
                                        "Texte normal ligne 2",
                                        html.Br(),
                                        "Texte normal ligne 3"
                                    ])
                                )
                            ]
                        )   
        ]
    )