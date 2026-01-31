from dash import html

def create_footer():
    return html.Footer(
        className="footer",
        children=[
            html.Div(
                className="footer_top",
                children=[
                    html.Img(
                        className="footer_logo",
                        src="/assets/images/monogram.png",
                        alt="Logo"
                    ),
                    html.Div(
                        className="footer_icons",
                        children=[
                            html.A(
                                href="https://github.com/clemence-carcanade/Dashboard_Gender_Gap",
                                target="_blank",
                                children=html.Img(className="logo_links", src="/assets/images/github.png", alt="GitHub")
                            ),
                            html.A(
                                href="https://www.figma.com/design/ZsVodzjamAdu6Hm0btIBPQ/DashBoard_Gender_Gap?node-id=0-1&t=52s2Xcpp67KOVo5I-1",
                                target="_blank",
                                children=html.Img(className="logo_links", src="/assets/images/figma.png", alt="Figma")
                            ),
                        ]
                    ),
                    html.Div(
                        className="footer_links",
                        children=[
                            html.Ul([
                                html.Li(html.B("Thaïs Castillo")),
                                html.Li("Projet Manager Apprentice - Crédit Agricole"),
                                html.Li("thais.castillo@edu.esiee.fr"),
                            ]),
                            html.Ul([
                                html.Li(html.B("Clémence Carcanade")),
                                html.Li("Software and IA Engineer Apprentice - Dassault Systèmes"),
                                html.Li("clemence.carcanade@edu.esiee.fr"),
                            ])
                        ]
                    )
                ]
            ),
            html.Div(
                "Copyright © 2026 — Designed by Thaïs Castillo & Clémence Carcanade",
                className="footer_bottom"
            )
        ]
    )
