from dash import html

def create_card(*children_content):
    return html.Div(
        className="card",
        children=list(children_content)
    )