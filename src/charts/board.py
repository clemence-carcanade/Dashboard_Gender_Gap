from dash import html, callback
from dash.dependencies import Input, Output
from src.components.segmented_control import create_segmented_control
from src.utils.get_data import get_gii_long_format, get_stem_data

df_gii_long = get_gii_long_format()
df_stem = get_stem_data()

df_stem = df_stem[~df_stem["Year"].isin([1998, 2019])]

VALUE_COL = "Female share of graduates from Science, Technology, Engineering and Mathematics (STEM) programmes, tertiary (%)"

def layout(data_type="gii"):
    if data_type == "gii":
        title_leaders = "Leading Countries in Gender Equality"
        title_lowest = "Lowest Countries in Gender Equality"
        source_title = "Kaggle"
        source_url = "https://www.kaggle.com/code/anoopjohny/gender-inequality-study"
    else:  # stem
        title_leaders = "Countries with the Highest Women's Share in STEM"
        title_lowest = "Countries with the Lowest Women's Share in STEM"
        source_title = "Our World in Data"
        source_url = "https://ourworldindata.org/grapher/share-graduates-stem-female"
    
    return html.Div(
        className="ranking_container",
        children=[
            create_segmented_control(
                className="bookmarks",
                id=f"top_selector_{data_type}",
                options=["🏆", "🆘"]
            ),
            html.Div(
                id=f"ranking_display_{data_type}",
                children=[
                    html.Div(
                        id=f"leaders_section_{data_type}",
                        className="leaders",
                        children=[
                            html.H3(title_leaders),
                            html.Span(id=f"year_rank_leaders_{data_type}", className="year_rank"),
                            html.Ul(id=f"ranking_leaders_{data_type}", className="ranking_list"),
                        ]
                    ),
                    html.Div(
                        id=f"lowest_section_{data_type}",
                        className="lowest",
                        style={"display": "none"},
                        children=[
                            html.H3(title_lowest),
                            html.Span(id=f"year_rank_lowest_{data_type}", className="year_rank"),
                            html.Ul(id=f"ranking_lowest_{data_type}", className="ranking_list"),
                        ]
                    )
                ]
            ),
            html.A(
                source_title,
                href=source_url,
                target="_blank",
                className="source",
            ),
        ]
    )

@callback(
    [Output("leaders_section_gii", "style"),
     Output("lowest_section_gii", "style")],
    Input("top_selector_gii", "value")
)
def toggle_gii_display(selected):
    if selected == "🏆":
        return {"display": "block"}, {"display": "none"}
    else:
        return {"display": "none"}, {"display": "block"}

@callback(
    Output("ranking_leaders_gii", "children"),
    Input({"type": "year-slider", "id": "gii"}, "value")
)
def update_gii_leaders(year_selected):
    df_year = (
        df_gii_long[df_gii_long["Year"] == year_selected]
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
    Output("ranking_lowest_gii", "children"),
    Input({"type": "year-slider", "id": "gii"}, "value")
)
def update_gii_lowest(year_selected):
    df_year = (
        df_gii_long[df_gii_long["Year"] == year_selected]
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
    [Output("year_rank_leaders_gii", "children"),
     Output("year_rank_lowest_gii", "children")],
    Input({"type": "year-slider", "id": "gii"}, "value")
)
def update_gii_year(year_selected):
    year_str = str(year_selected)
    return year_str, year_str

@callback(
    [Output("leaders_section_stem", "style"),
     Output("lowest_section_stem", "style")],
    Input("top_selector_stem", "value")
)
def toggle_stem_display(selected):
    if selected == "🏆":
        return {"display": "block"}, {"display": "none"}
    else:
        return {"display": "none"}, {"display": "block"}

@callback(
    Output("ranking_leaders_stem", "children"),
    Input({"type": "year-slider", "id": "stem"}, "value")
)
def update_stem_leaders(year_selected):
    df_year = (
        df_stem[df_stem["Year"] == year_selected]
        .dropna(subset=[VALUE_COL])
        .sort_values(VALUE_COL, ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    return [
        html.Li(
            className="ranking_item",
            children=[
                html.Span(f"{i+1}.", className="ranking_rank"),
                html.Span(row.Entity, className="ranking_country"),
                html.Span(f"{row[VALUE_COL]:.1f}%", className="ranking_value"),
            ],
        )
        for i, row in df_year.iterrows()
    ]

@callback(
    Output("ranking_lowest_stem", "children"),
    Input({"type": "year-slider", "id": "stem"}, "value")
)
def update_stem_lowest(year_selected):
    df_year = (
        df_stem[df_stem["Year"] == year_selected]
        .dropna(subset=[VALUE_COL])
    )
    
    df_year = df_year[df_year[VALUE_COL] > 0]
    
    df_year = (
        df_year
        .sort_values(VALUE_COL)
        .head(10)
        .reset_index(drop=True)
    )

    return [
        html.Li(
            className="ranking_item",
            children=[
                html.Span(f"{i+1}.", className="ranking_rank"),
                html.Span(row.Entity, className="ranking_country"),
                html.Span(f"{row[VALUE_COL]:.1f}%", className="ranking_value"),
            ],
        )
        for i, row in df_year.iterrows()
    ]

@callback(
    [Output("year_rank_leaders_stem", "children"),
     Output("year_rank_lowest_stem", "children")],
    Input({"type": "year-slider", "id": "stem"}, "value")
)
def update_stem_year(year_selected):
    year_str = str(year_selected)
    return year_str, year_str