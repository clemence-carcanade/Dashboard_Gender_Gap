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
                                html.P("Votre texte principal ici. Ce conteneur peut contenir autant de texte que nécessaire.")
                            ]
                        ),
                        # Petits conteneurs alignés en dessous
                ]
            ),
            html.Div(
                            className="cards-row",
                            children=[
                                create_card(html.P("Texte 1")),
                                create_card(html.P("Texte 2")),
                                create_card(html.P("Texte 3")),  # Vous pouvez en ajouter plus
                            ]
                        )   
        ]
    )