from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from src.components.navbar import create_navbar
from src.pages.home import layout as home_layout
from src.pages.about import layout as about_layout
from src.components.footer import create_footer
app = Dash(__name__, suppress_callback_exceptions=True, assets_folder="src/assets", title="Gender Gap in STEM")

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    create_navbar(),
    html.Div(id='page-content'),
    create_footer()
])

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == "/":
        return home_layout()
    elif pathname == "/about":
        return about_layout()
    else:
        return html.H1("404 : Not found")

if __name__ == "__main__":
    app.run(debug=True)