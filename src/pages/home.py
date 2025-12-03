from dash import html

def layout():
    return html.Div(
        className="home-page",
        children=[
            html.H1("Where are the women in science?")
        ]
    )