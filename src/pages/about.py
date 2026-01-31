from dash import html
from src.components.card import create_card

def layout():
    return html.Div(
        className="about_page",
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
                    "--top": "600px",
                    "--left": "100px"
                }
            ),
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--blue)",
                    "--top": "350px",
                    "--right": "50px"
                }
            ),
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--blue)",
                    "--top": "900px",
                    "--right": "600px"
                }
            ),
            html.Div(
                className="content_row",
                children=[
                        html.Img(
                            src="/assets/images/illustration.png",
                            className="about_img",
                            alt="Illustration of our work group"
                        ),
                        create_card(
                            html.H1("About us"),
                            html.P(["This dashboard was developed as part of an academic project at ", html.B("ESIEE Paris"), ", within the Computer Science and Applications apprenticeship program. It was created by Clémence Carcanade, apprentice Software & AI Engineer at Dassault Systèmes, and Thaïs Castillo, apprentice Project Manager at Crédit Agricole Payment Services."]),
                            html.P(["As two future engineers, we are particularly committed to questions of ", html.B("gender equality in science"), ", a field where women remain underrepresented despite their central role in innovation."])
                        ),
                ]
            ),
            create_card(
                html.H3("Why gender equality in STEM matters ?"),
                html.P(["Innovation is often presented as a driver of economic growth and social progress. Yet, in many countries, access to scientific education and technological careers remains deeply unequal. Gender disparities in STEM are not only an issue of fairness: they directly affect the ", html.B("long-term development of our societies.")]),
                html.P("Understanding where these gaps persist—and how they vary across regions—helps highlight the structural barriers women face and the progress that still needs to be made. By combining global indicators with a focused analysis of France, this project aims to contribute to a clearer, data-driven understanding of these inequalities, and to a broader reflection on how society can—and must—become more inclusive.")
            ),
            html.Div(
                className="cards_row",
                children=[
                    create_card(
                        html.H3("Project Organization"),
                        html.Ul([
                            html.Li([
                                html.B("Thaïs Castillo — "),
                                "Produced the visualizations for the world analysis and for the fields of study chosen by women in France, and wrote the analytical interpretations of all charts, grounding the data in a broader social and political perspective."
                            ]),
                            html.Li([
                                html.B("Clémence Carcanade — "),
                                "Developed the visualizations on education and wage gaps in France and designed the entire front-end of the dashboard, transforming data into an coherent and engaging public-facing tool."
                            ]),
                        ]),
                        html.P("This collaboration reflects our shared belief that technical skills and social engagement are not separate, but complementary.")
                    ),
                    html.Img(
                        src="/assets/images/tools.png",
                        className="about_img",
                        alt="Tools used for the project"
                    ),
                ]
            ),
            create_card(
                html.H3("Data and Sources"),
                html.P(["This dashboard is based on ", html.B("publicly available datasets"), " from international and national institutions. Visualizations are designed to make complex indicators more accessible while preserving data integrity."])
            )
        ]
    )