from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from src.components.navbar import create_navbar
from src.pages.home import layout as home_layout

app = Dash(__name__, suppress_callback_exceptions=True, assets_folder="src/assets")

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(className="background-glow"),
    create_navbar(),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == "/":
        return home_layout()
    elif pathname == "/about":
        return html.H1("About")
    else:
        return html.H1("404 : Not found")

if __name__ == "__main__":
    app.run(debug=True)