from dash import html

def create_navbar():
    return html.Nav(
        className="navbar",
        children=[
            html.Ul([
                html.Li(html.A("DashBoard - Gender Gap in STEM", href="/")),
                html.Li(html.A("About", href="/about"))
            ])
        ]
    )
