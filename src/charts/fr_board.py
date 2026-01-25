from dash import html, callback
from dash.dependencies import Input, Output
import pandas as pd
from src.components.segmented_control import create_segmented_control

df = pd.read_csv("data/cleaned/fr_regions_gender_inequality_cleaned.csv")

REGION_NAMES = ['Île-de-France', 'Centre-Val de Loire', 'Bourgogne-Franche-Comté', 
                'Normandie', 'Hauts-de-France', 'Grand Est', 'Pays de la Loire', 
                'Bretagne', 'Nouvelle-Aquitaine', 'Occitanie', 'Auvergne-Rhône-Alpes',
                'Provence-Alpes-Côte d\'Azur', 'Corse', 'France métropolitaine hors Ile-de-France',
                'France métropolitaine', 'Guadeloupe', 'Martinique', 'Guyane', 'La Réunion',
                'DROM hors Mayotte', 'France hors Mayotte']

df_departments = df[~df['Region'].isin(REGION_NAMES)].copy()
df_departments['Salary_Gap_2022_abs'] = df_departments['Salary_Gap_2022'].abs()

# ----------------------------
# BOARD LAYOUT
# ----------------------------

def layout():
    """
    Crée un board de classement qui s'adapte automatiquement 
    au metric sélectionné (Education ou Salary)
    """
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
            )
        ]
    )

# ----------------------------
# TOGGLE DISPLAY CALLBACK
# ----------------------------

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

# ----------------------------
# UPDATE RANKINGS CALLBACK
# ----------------------------

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
    """
    Met à jour les rankings en fonction du metric sélectionné
    """
    if metric == "Disparity in Education":
        # EDUCATION (2021)
        title_leaders = "Departments with Highest Women's Share in Higher Education"
        title_lowest = "Departments with Lowest Women's Share in Higher Education"
        year_str = "2021"
        
        df_leaders = (
            df_departments
            .dropna(subset=["Education_Gap_2021"])
            .sort_values("Education_Gap_2021", ascending=False)
            .head(10)
            .reset_index(drop=True)
        )
        
        df_lowest = (
            df_departments
            .dropna(subset=["Education_Gap_2021"])
            .sort_values("Education_Gap_2021")
            .head(10)
            .reset_index(drop=True)
        )
        
        ranking_leaders = [
            html.Li(
                className="ranking_item",
                children=[
                    html.Span(f"{i+1}.", className="ranking_rank"),
                    html.Span(row['Region'], className="ranking_country"),
                    html.Span(f"{row['Education_Gap_2021']:.1f}%", className="ranking_value"),
                ]
            ) for i, row in df_leaders.iterrows()
        ]
        
        ranking_lowest = [
            html.Li(
                className="ranking_item",
                children=[
                    html.Span(f"{i+1}.", className="ranking_rank"),
                    html.Span(row['Region'], className="ranking_country"),
                    html.Span(f"{row['Education_Gap_2021']:.1f}%", className="ranking_value"),
                ]
            ) for i, row in df_lowest.iterrows()
        ]
        
    else:  # "Wage Inequality"
        # SALARY (2022)
        title_leaders = "Departments with Smallest Gender Pay Gap"
        title_lowest = "Departments with Largest Gender Pay Gap"
        year_str = "2022"
        
        df_leaders = (
            df_departments
            .dropna(subset=["Salary_Gap_2022_abs"])
            .sort_values("Salary_Gap_2022_abs")
            .head(10)
            .reset_index(drop=True)
        )
        
        df_lowest = (
            df_departments
            .dropna(subset=["Salary_Gap_2022_abs"])
            .sort_values("Salary_Gap_2022_abs", ascending=False)
            .head(10)
            .reset_index(drop=True)
        )
        
        ranking_leaders = [
            html.Li(
                className="ranking_item",
                children=[
                    html.Span(f"{i+1}.", className="ranking_rank"),
                    html.Span(row['Region'], className="ranking_country"),
                    html.Span(f"{row['Salary_Gap_2022_abs']:.1f}%", className="ranking_value"),
                ]
            ) for i, row in df_leaders.iterrows()
        ]
        
        ranking_lowest = [
            html.Li(
                className="ranking_item",
                children=[
                    html.Span(f"{i+1}.", className="ranking_rank"),
                    html.Span(row['Region'], className="ranking_country"),
                    html.Span(f"{row['Salary_Gap_2022_abs']:.1f}%", className="ranking_value"),
                ]
            ) for i, row in df_lowest.iterrows()
        ]
    
    return (
        title_leaders,
        title_lowest,
        ranking_leaders,
        ranking_lowest,
        year_str,
        year_str
    )