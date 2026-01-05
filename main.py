from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from src.components.navbar import create_navbar
from src.pages.home import layout as home_layout
from src.charts.gii_world_map import layout as gii_map_layout
from src.charts.gii_board import layout as gii_board_layout
from src.charts.gii_histogram import layout as gii_bar_layout

app = Dash(__name__, suppress_callback_exceptions=True, assets_folder="src/assets")

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
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

@app.callback(
    Output("gii_container", "children"),
    Input("view_selector", "value")
)
def update_chart(view_selected):
    if view_selected == "🌍 Map":
        return [gii_map_layout(), gii_board_layout()]
    else:  # "Bars"
        return [gii_bar_layout(), gii_board_layout()]
    
if __name__ == "__main__":
    app.run(debug=True)