from dash import html, dcc, callback, Output, Input, State

years = []

def create_gii_slider(years_list):
    global years
    years = years_list
    
    return html.Div(
        className="slider_container",
        children=[
            html.Button("▶", id="play_pause_button", n_clicks=0),
            dcc.Interval(
                id="interval",
                interval=500,
                n_intervals=0,
                disabled=True
            ),
            dcc.Slider(
                id="gii_slider",
                min=int(years[0]),
                max=int(years[-1]),
                step=1,
                value=int(years[-1]),
                marks={
                    int(years[0]): str(years[0]),
                    int(years[-1]): str(years[-1]),
                },
                tooltip={
                    "placement": "bottom",
                    "always_visible": False
                },
            )
        ]
    )

@callback(
    Output("interval", "disabled"),
    Output("play_pause_button", "children"),
    Input("play_pause_button", "n_clicks"),
    State("interval", "disabled")
)
def toggle_play_pause(n_clicks, disabled):
    if n_clicks == 0:
        return True, "▶"
    new_disabled = not disabled
    new_label = "⏸" if not new_disabled else "▶"
    return new_disabled, new_label

@callback(
    Output("gii_slider", "value"),
    Input("interval", "n_intervals"),
    State("gii_slider", "value")
)
def update_slider(n_intervals, current_year):
    if not years or current_year not in years:
        return years[0] if years else current_year
    idx = years.index(current_year)
    if idx + 1 >= len(years):
        return years[0]
    return years[idx + 1]

@callback(
    Output("gii_slider", "marks"),
    Input("gii_slider", "value"),
)
def update_slider_marks(current_year):
    if not years:
        return {}
    return {
        int(years[0]): str(years[0]),
        int(years[-1]): str(years[-1]),
        int(current_year): str(current_year),
    }