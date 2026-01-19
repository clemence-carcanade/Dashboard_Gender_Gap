from dash import html, dcc

def create_segmented_control(options, className, id=None):
    return html.Div(
        className=className,
        children=[
            dcc.RadioItems(
                id=id,
                options=[{"label": opt, "value": opt} for opt in options],
                value=options[0],
                className="radio_group",
            )
        ]
    )
