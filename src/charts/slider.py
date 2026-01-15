from dash import html, dcc, callback, Output, Input, State, MATCH

def create_slider(years, slider_id):
    return html.Div(
        className="slider_container",
        children=[
            html.Button(
                "▶",
                id={"type": "play-pause", "id": slider_id},
                n_clicks=0,
            ),
            dcc.Interval(
                id={"type": "interval", "id": slider_id},
                interval=500,
                n_intervals=0,
                disabled=True,
            ),
            dcc.Slider(
                id={"type": "year-slider", "id": slider_id},
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
            ),
            dcc.Store(
                id={"type": "years-store", "id": slider_id},
                data=years
            )
        ]
    )

@callback(
    Output({"type": "interval", "id": MATCH}, "disabled"),
    Output({"type": "play-pause", "id": MATCH}, "children"),
    Input({"type": "play-pause", "id": MATCH}, "n_clicks"),
    State({"type": "interval", "id": MATCH}, "disabled"),
)
def toggle_play_pause(n_clicks, disabled):
    if n_clicks == 0:
        return True, "▶"
    new_disabled = not disabled
    return new_disabled, "⏸" if not new_disabled else "▶"

@callback(
    Output({"type": "year-slider", "id": MATCH}, "value"),
    Input({"type": "interval", "id": MATCH}, "n_intervals"),
    State({"type": "year-slider", "id": MATCH}, "value"),
    State({"type": "years-store", "id": MATCH}, "data"),
)
def update_slider(_, current_year, years):
    if current_year not in years:
        return years[0]

    idx = years.index(current_year)
    return years[(idx + 1) % len(years)]

@callback(
    Output({"type": "year-slider", "id": MATCH}, "marks"),
    Input({"type": "year-slider", "id": MATCH}, "value"),
    State({"type": "years-store", "id": MATCH}, "data"),
)
def update_slider_marks(current_year, years):
    return {
        int(years[0]): str(years[0]),
        int(years[-1]): str(years[-1]),
        int(current_year): str(current_year),
    }