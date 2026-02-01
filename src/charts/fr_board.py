from dash import html, callback
from dash.dependencies import Input, Output
from src.components.segmented_control import create_segmented_control
from src.utils.get_data import get_fr_departments_data

df_departments = get_fr_departments_data()

def layout():
    return html.Div(
        className="ranking_container",
        children=[
            create_segmented_control(
                className="bookmarks",
                id="top_selector_france",
                options=["🏆", "🆘"]
            ),
            html.Div(
                id="ranking_display_france",
                children=[
                    html.Div(
                        id="leaders_section_france",
                        className="leaders",
                        children=[
                            html.H3(id="title_leaders_france"),
                            html.Span(id="year_rank_leaders_france", className="year_rank"),
                            html.Ul(id="ranking_leaders_france", className="ranking_list"),
                        ]
                    ),
                    html.Div(
                        id="lowest_section_france",
                        className="lowest",
                        style={"display": "none"},
                        children=[
                            html.H3(id="title_lowest_france"),
                            html.Span(id="year_rank_lowest_france", className="year_rank"),
                            html.Ul(id="ranking_lowest_france", className="ranking_list"),
                        ]
                    )
                ]
            ),
            html.A(
                "INSEE",
                href="https://www.insee.fr/fr/statistiques/2513786#consulter",
                target="_blank",
                className="source fr",
            ),
        ]
    )


@callback(
    [Output("leaders_section_france", "style"),
     Output("lowest_section_france", "style")],
    Input("top_selector_france", "value")
)
def toggle_france_display(selected):
    if selected == "🏆":
        return {"display": "block"}, {"display": "none"}
    else:
        return {"display": "none"}, {"display": "block"}

def _create_ranking_items(df_sorted, value_column):
    return [
        html.Li(
            className="ranking_item",
            children=[
                html.Span(f"{i+1}.", className="ranking_rank"),
                html.Span(row['Region'], className="ranking_country"),
                html.Span(f"{row[value_column]:.1f}%", className="ranking_value"),
            ]
        ) for i, row in df_sorted.iterrows()
    ]

@callback(
    [Output("title_leaders_france", "children"),
     Output("title_lowest_france", "children"),
     Output("ranking_leaders_france", "children"),
     Output("ranking_lowest_france", "children"),
     Output("year_rank_leaders_france", "children"),
     Output("year_rank_lowest_france", "children")],
    [Input("france_data_selector", "value"),
     Input("top_selector_france", "value")]
)
def update_france_rankings(metric, _):
    if metric == "Disparity in Education":
        title_leaders = "Departments with Highest Women's Share in Higher Education"
        title_lowest = "Departments with Lowest Women's Share in Higher Education"
        year_str = "2021"
        column = "Education_Gap_2021"

        df_leaders = (
            df_departments
            .dropna(subset=[column])
            .sort_values(column, ascending=False)
            .head(10)
            .reset_index(drop=True)
        )

        df_lowest = (
            df_departments
            .dropna(subset=[column])
            .sort_values(column, ascending=True)
            .head(10)
            .reset_index(drop=True)
        )
        
    else:  # "Wage Inequality"
        title_leaders = "Departments with Smallest Gender Pay Gap"
        title_lowest = "Departments with Largest Gender Pay Gap"
        year_str = "2022"
        column = "Salary_Gap_2022_abs"
        
        df_leaders = (
            df_departments
            .dropna(subset=[column])
            .sort_values(column, ascending=True)
            .head(10)
            .reset_index(drop=True)
        )
        
        df_lowest = (
            df_departments
            .dropna(subset=[column])
            .sort_values(column, ascending=False)
            .head(10)
            .reset_index(drop=True)
        )
    
    ranking_leaders = _create_ranking_items(df_leaders, column)
    ranking_lowest = _create_ranking_items(df_lowest, column)
    
    return (
        title_leaders,
        title_lowest,
        ranking_leaders,
        ranking_lowest,
        year_str,
        year_str
    )