from dash import html

def create_navbar():
    return html.Nav(
        className="navbar",
        children=[
            html.Ul(
                className="navbar_list",
                children=[
                    html.Div(
                        className="navbar_left",
                        children=[
                            html.Li(html.A(html.B("DashBoard - Gender Gap in STEM"), href="/")),
                            html.Li(html.A("World", href="/#world_anchor")),
                            html.Li(html.A("France", href="/#france_anchor")),
                        ],
                    ),
                    html.Div(
                        className="navbar_right",
                        children=[
                            html.Li(html.A(html.B("About"), href="/about")),
                        ],
                    ),
                ],
            )
        ],
    )
