from dash import html
from src.components.card import create_card

def layout():
    return html.Div(
        className="world_analysis_written",
        children=[
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--blue)",
                    "--top": "3600px",
                    "--left": "150px"
                }
            ),
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--pink)",
                    "--top": "4100px",
                    "--right": "300px"
                }
            ),
            create_card(
                html.P(["After exploring gender equality worldwide, France reveals a familiar yet striking paradox. Across all departments, women are consistently more likely than men to pursue higher education. Yet when it comes to wages, the pattern reverses: everywhere in France, men continue to earn more than women. ", html.B("In short, women study more, but men are still paid better.")])
            ),
            html.Div(
                className="illustrated_text",
                children=[
                    create_card(
                        html.P(["Geography helps explain part of this contradiction. Departments with the highest shares of women in higher education—such as Hautes-Alpes, Lozère or Haute-Loire—tend to host training programmes linked to traditionally ", html.B("feminised professions"), ", particularly in healthcare and nursing. By contrast, engineering schools and other male-dominated fields are largely ", html.B("concentrated in major urban centres"), ", especially Paris. This urban concentration places Île-de-France departments among those with the lowest proportions of women in higher education."]),
                        html.P(["Mobility also plays a key role. Many young women leave their home departments to study near large cities, while those living farther from metropolitan areas are more likely to enrol locally. Research by CEREQ shows that ", html.B("financial constraints and safety concerns"), " often limit women’s mobility at the start of their careers, shaping these territorial disparities."])
                    ),
                    html.Img(
                        src="/assets/images/education.png",
                        className="icon_3d",
                        alt="diploma 3d icon"
                    ),
                ]
            ),
            html.Div(
                className="illustrated_text",
                children=[
                    html.Img(
                        src="/assets/images/job.png",
                        className="icon_3d",
                        alt="job 3d icon"
                    ),
                    create_card(
                        html.P(["Turning to wage equality, departments with the smallest gender pay gaps—such as Hautes-Alpes, Deux-Sèvres, and Creuse—are characterised by a strong presence of ", html.B("public-sector employment"), ". In these areas, wages are governed by fixed and transparent pay scales, which helps limit gender disparities. In contrast, ", html.B("private-sector jobs"), ", which are more prevalent in large urban centres, tend to exhibit wider pay gaps. Moreover, high-paying and senior positions such as executives and directors remain overwhelmingly male-dominated and are primarily located in metropolitan areas, further widening the observed salary differences."]),
                    ),
                ]
            ),
            create_card(
                html.H3(
                    className="h3_normal",
                    children=[
                        html.P("France therefore illustrates a structural imbalance: women’s educational advantage does not translate into economic equality. Sectoral segregation and persistent gender norms continue to shape unequal outcomes—reminding us that education alone is not enough to close the gender gap.")
                    ]
                )
            ),
        ]
    )