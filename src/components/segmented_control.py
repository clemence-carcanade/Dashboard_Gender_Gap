from dash import html, dcc

def create_segmented_control(options):
    return html.Div(
        className="segmented_control",
        children=[
            dcc.RadioItems(
                options=[{"label": opt, "value": opt} for opt in options],
                value=options[0],
                className="radio_group",
            )
        ]
    )
