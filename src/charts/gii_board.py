from dash import html, callback
from dash.dependencies import Input, Output
import pandas as pd

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
            html.H3("🏆 Leading Countries in Gender Equality"),
            html.Span(id="year_rank", className="year_rank"),
            html.Ul(id="gii_ranking", className="ranking_list"),
        ]
    )


@callback(
    Output("gii_ranking", "children"),
    Input("gii_slider", "value")
)
def update_ranking(year_selected):
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
    Output("year_rank", "children"),
    Input("gii_slider", "value")
)
def update_year(year_selected):
    return str(year_selected)