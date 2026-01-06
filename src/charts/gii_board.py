from dash import html, callback
from dash.dependencies import Input, Output
import pandas as pd
from src.components.segmented_control import create_segmented_control

df = pd.read_csv("data/raw/world_GII.csv")

gii_columns = [c for c in df.columns if c.startswith("Gender Inequality Index")]

df_long = df.melt(
    id_vars=["ISO3", "Country", "Continent"],
    value_vars=gii_columns,
    var_name="Year",
    value_name="GII"
)

df_long["Year"] = df_long["Year"].str.extract(r"(\d{4})").astype(int)

def layout():
    return html.Div(
        className="ranking_container",
        children=[
            create_segmented_control(
                className="bookmarks",
                id="top_selector",
                options=["🏆", "🆘"]
            ),
            html.Div(
                id="ranking_display",
                children=[
                    html.Div(
                        id="leaders_section",
                        className="leaders",
                        children=[
                            html.H3("Leading Countries in Gender Equality"),
                            html.Span(id="year_rank_leaders", className="year_rank"),
                            html.Ul(id="gii_ranking_leaders", className="ranking_list"),
                        ]
                    ),
                    html.Div(
                        id="lowest_section",
                        className="lowest",
                        style={"display": "none"},
                        children=[
                            html.H3("Lowest Countries in Gender Equality"),
                            html.Span(id="year_rank_lowest", className="year_rank"),
                            html.Ul(id="gii_ranking_lowest", className="ranking_list"),
                        ]
                    )
                ]
            )
        ]
    )

@callback(
    [Output("leaders_section", "style"),
     Output("lowest_section", "style")],
    Input("top_selector", "value")
)
def toggle_ranking_display(selected):
    if selected == "🏆":
        return {"display": "block"}, {"display": "none"}
    else:
        return {"display": "none"}, {"display": "block"}

@callback(
    Output("gii_ranking_leaders", "children"),
    Input("gii_slider", "value")
)
def update_ranking_leaders(year_selected):
    df_year = (
        df_long[df_long["Year"] == year_selected]
        .dropna(subset=["GII"])
        .sort_values("GII")
        .head(10)
        .reset_index(drop=True)
    )

    return [
        html.Li(
            className="ranking_item",
            children=[
                html.Span(f"{i+1}.", className="ranking_rank"),
                html.Span(row.Country, className="ranking_country"),
                html.Span(f"{row.GII:.3f}", className="ranking_value"),
            ],
        )
        for i, row in df_year.iterrows()
    ]

@callback(
    Output("gii_ranking_lowest", "children"),
    Input("gii_slider", "value")
)
def update_ranking_lowest(year_selected):
    df_year = (
        df_long[df_long["Year"] == year_selected]
        .dropna(subset=["GII"])
        .sort_values("GII", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    return [
        html.Li(
            className="ranking_item",
            children=[
                html.Span(f"{i+1}.", className="ranking_rank"),
                html.Span(row.Country, className="ranking_country"),
                html.Span(f"{row.GII:.3f}", className="ranking_value"),
            ],
        )
        for i, row in df_year.iterrows()
    ]

@callback(
    [Output("year_rank_leaders", "children"),
     Output("year_rank_lowest", "children")],
    Input("gii_slider", "value")
)
def update_year(year_selected):
    year_str = str(year_selected)
    return year_str, year_str