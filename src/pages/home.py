from dash import html, callback
from dash.dependencies import Input, Output
from src.components.card import create_card
from src.components.segmented_control import create_segmented_control
from src.charts.gii_world_map import layout as gii_map_layout
from src.charts.gii_histogram import layout as gii_bar_layout
from src.charts.stem_histogram import layout as stem_bars_layout
from src.charts.stem_world_map import layout as stem_map_layout
from src.charts.board import layout as board_layout
from src.pages.world_analysis import layout as world_layout

from src.charts.fr_histogram import education_bars_layout as education_bars_layout
from src.charts.fr_map import education_map_layout as education_map_layout
from src.charts.fr_board import layout as fr_board_layout
from src.charts.fr_university import layout as university_layout
from src.charts.fr_phd import layout as phd_layout
from src.pages.france_analysis import layout as france_layout
from src.pages.study_analysis import layout as study_layout

def layout():
    return html.Div(
        className="home-page",
        children=[
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--pink)",
                    "--top": "60px",
                    "--right": "550px"
                }
            ),
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--pink)",
                    "--top": "350px",
                    "--left": "50px"
                }
            ),
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--blue)",
                    "--top": "575px",
                    "--right": "450px"
                }
            ),
            html.Div(
                className="title",
                children=[
                    create_card(
                        html.H1("\"Where are the women in science?\""),
                        html.H3("This question, still asked far too often, highlights the persistent gender inequalities in scientific fields."),
                        html.P(["As part of a student project focused on creating an interactive dashboard in Python, we chose to explore these inequalities in depth. The aim of this work is to shed light on the ", html.B("disparities between women and men in science"), ", both in France and worldwide, using reliable data and recognized studies. We selected this topic because it resonates strongly with us: as women studying in digital and engineering fields, we are directly concerned by the underrepresentation of women in these domains, which remain largely male-dominated. This project is therefore both an analytical exercise and a personal commitment, intended to raise awareness and inform through educational data visualizations."])
                    ),
                    html.Img(
                        src="/assets/images/gender_balance.png",
                        className="gender-image",
                        alt="gender_equality_balance"
                    )
                ]
            ),
            html.H1(
                "World Analysis",
                id="world_anchor",
                style={"textAlign": "center",
                       "marginTop": "5px",
                       "marginBottom": "5px",
                       "scrollMarginTop": "135px"}
            ),
            html.Div(
                className="quote",
                children=[
                    create_card(
                        html.Img(
                            src="/assets/images/undp.jpg",
                            className="undp-logo",
                            alt="undp_logo"
                        ),
                        html.H3(
                            className="h3_normal",
                            children=[
                                "“",
                                html.I(
                                    "GII is a composite metric of gender inequality using three dimensions: reproductive health, empowerment and the labour market. "
                                    "A low GII value indicates low inequality between women and men, and vice-versa."
                                ),
                                "” UNDP"
                            ]
                        )
                    ),
                ]
            ),
            create_segmented_control(
                options=["Gender Inequality Index", "Women's Share in STEM"],
                className="segmented_control",
                id="data_selector"
            ),
            html.Div(
                className="world_analysis",
                children=[
                    create_segmented_control(
                        options=["🌍 Map", "📊 Bars"],
                        className="segmented_control small",
                        id="view_selector"
                    ),
                    html.Div(id="visualization_container")
                ]
            ),
            world_layout(),
            html.H1(
                "France Analysis",
                id="france_anchor",
                style={"textAlign": "center",
                       "marginTop": "5px",
                       "marginBottom": "5px",
                       "scrollMarginTop": "135px"}
            ),
            create_segmented_control(
                options=["Disparity in Education", "Wage Inequality"],
                className="segmented_control",
                id="france_data_selector"
            ),
            html.Div(
                className="world_analysis",
                children=[
                    create_segmented_control(
                        options=["🌍 Map", "📊 Bars"],
                        className="segmented_control small",
                        id="france_view_selector"
                    ),
                    html.Div(id="france_visualization_container")
                ]
            ),
            france_layout(),
            create_segmented_control(
                options=["Bachelor's Degree Fields", "PhD Fields"],
                className="segmented_control",
                id="france_study_data_selector"
            ),
            html.Div(
                className="study_analysis",
                children=[
                    html.Div(id="france_study_visualization_container")
                ]
            ),
            study_layout(),
            html.H1(
                "Conclusion",
                style={"textAlign": "center",
                       "marginTop": "5px",
                       "marginBottom": "5px"}
            ),
            create_card(
                html.P(["Across countries and regions, our analysis reveals a consistent pattern: gender inequalities in science are shaped not only by access to education, but also by economic structures, social norms, and deeply rooted stereotypes. While women increasingly outperform men in educational attainment—both globally and in France—this advantage does not translate into equal representation in STEM fields or into equal economic outcomes."]),
                html.P(["From the Gender Inequality Index to national and regional data, the same dynamics emerge: women remain concentrated in certain disciplines, while technological and high-paying fields continue to be largely male-dominated. Whether driven by poverty, social constraints, or the Gender Equality Paradox observed in the most egalitarian societies, these inequalities persist across contexts."]),
                html.P(html.B("Ultimately, closing the gender gap in science requires more than formal equality or educational access. It calls for a transformation of cultural norms, institutional practices, and professional environments so that women can not only enter scientific fields, but also thrive and fully contribute to innovation.")),
            ),
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--blue)",
                    "--top": "6000px",
                    "--right": "50px"
                }
            ),
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--pink)",
                    "--top": "6040px",
                    "--left": "50px"
                }
            ),
        ]
    )

@callback(
    Output("visualization_container", "children"),
    [Input("data_selector", "value"),
     Input("view_selector", "value")]
)
def update_visualization(data_type, view_type):
    if data_type == "Gender Inequality Index":
        if view_type == "🌍 Map":
            return html.Div(
                className="world_container",
                children=[
                    gii_map_layout(),
                    board_layout("gii"),
                ]
            )
        else:
            return html.Div(
                className="world_container",
                children=[
                    gii_bar_layout(),
                    board_layout("gii"),
                ]
            )
    else:
        if view_type == "🌍 Map":
            return html.Div(
                className="world_container",
                children=[
                    stem_map_layout(),
                    board_layout("stem"),
                ]
            )
        else:
            return html.Div(
                className="world_container",
                children=[
                    stem_bars_layout(),
                    board_layout("stem"),
                ]
            )
        
@callback(
    Output("france_visualization_container", "children"),
    Input("france_data_selector", "value"),
    Input("france_view_selector", "value")
)
def update_visualization_france(data_type, view_type):

    if view_type == "🌍 Map":
        return html.Div(
            className="world_container",
            children=[
                education_map_layout(data_type),
                fr_board_layout()
            ]
        )

    else:  # 📊 Bars
        return html.Div(
            className="world_container",
            children=[
                education_bars_layout(data_type),
                fr_board_layout()
            ]
        )
    
@callback(
    Output("france_study_visualization_container", "children"),
    Input("france_study_data_selector", "value")
)
def update_visualization_study_france(data_type):

    if data_type == "Bachelor's Degree Fields":
        return university_layout()

    else:
        return phd_layout()