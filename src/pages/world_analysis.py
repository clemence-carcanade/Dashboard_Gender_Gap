from dash import html
from src.components.card import create_card

def layout():
    return html.Div(
        className="world_analysis_written",
        children=[
            create_card(
                html.H3("What lies behind the Data"),
                html.P(["Looking at the data from the ", html.B("Gender Inequality Index (GII)"), ", clear geographical patterns emerge. Nordic countries such as Denmark, Sweden, and Finland consistently rank among the most gender-equal nations, while many Sahelian countries tend to marginalise women and face persistent inequalities."])
            ),
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--pink)",
                    "--top": "1400px",
                    "--left": "50px"
                }
            ),
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--blue)",
                    "--top": "2000px",
                    "--right": "300px"
                }
            ),
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--pink)",
                    "--top": "2600px",
                    "--left": "50px"
                }
            ),
            html.Div(
                className="illustrated_text",
                children=[
                    create_card(
                        html.P(["At first glance, ", html.B("economic development"), " appears to play a decisive role in reducing gender inequalities. The contrast between Switzerland, with a GDP per capita of around $111,000, and Niger, with roughly $650, is striking. More generally, an individual living in a country at the top of the GII ranking is, on average, about sixty times ", html.B("wealthier"), " than someone living in a country at the bottom."]),
                        html.P(["However, economic wealth alone does not explain everything. Access to ", html.B("education"), " is another crucial factor. In many countries at the bottom of the ranking, such as Afghanistan and Guinea, girls’ education is often restricted, with families prioritising schooling for boys. As a result, girls are marginalised from an early age, depriving both themselves and their countries of future talent and innovation."])
                    ),
                    html.Img(
                        src="/assets/images/money.png",
                        className="icon_3d",
                        alt="diploma 3d icon"
                    ),
                ]
            ),
            html.Div(
                className="illustrated_text",
                children=[
                    html.Img(
                        src="/assets/images/politic.png",
                        className="icon_3d",
                        alt="politic 3d icon"
                    ),
                    create_card(
                        html.P([html.B("Social norms"), " further reinforce these inequalities. In Yemen and many Sahelian countries—including Mauritania, Niger, Gambia, Mali, and Burkina Faso—early marriage, often driven by extreme poverty, interrupts girls’ schooling prematurely. In contrast, in developed countries such as Denmark and Sweden, childcare systems and shared parental leave policies help women avoid having to choose between professional careers and family life."]),
                        html.P(["Political structures also play a decisive role. Gender equality rarely emerges by chance, especially when ", html.B("political systems"), " do not actively support it. Contrary to common assumptions, some countries such as Nigeria have introduced quotas for women in parliament. However, these positions often lack real decision-making power, limiting their impact on gender equality."])
                    ),
                ]
            ),
            create_card(
                html.H3(
                    className="h3_normal",
                    children=[
                        html.P("In today’s world, a society’s power is increasingly shaped by technological innovation. A country that excludes women from scientific and technological fields effectively excludes 50% of its potential for innovation.")
                    ]
                )
            ),
            html.Div(
                className="illustrated_text",
                children=[
                    create_card(
                        html.P(["Looking more closely at the share of women in STEM (Science, Technology, Engineering, and Mathematics) in 2016 reveals a striking and ", html.B("counterintuitive pattern"), ". Countries that are rarely associated with high levels of gender equality—such as Algeria, Niger, Syria, and Tunisia—ranked among those with the highest proportions of women in STEM fields. By contrast, nations commonly viewed as models of economic prosperity and gender progress, including Switzerland, appeared at the bottom of the ranking, alongside countries such as Chile and Burkina Faso. In the latter case, low female representation can be directly attributed to extreme poverty and limited access to education, which severely restrict girls’ schooling opportunities from an early age."]),
                        html.P(["However, low female participation in STEM does not always result from a lack of resources or formal equality. This apparent contradiction is captured by the concept of the ", html.B(html.I("Gender Equality Paradox")), ", identified by Gijsbert Stoet and David C. Geary in 2018. Their research shows that in the most gender-equal and affluent societies, women are less likely to pursue STEM careers. In countries such as Switzerland, where the standard of living is high and social safety nets are strong, women have greater freedom to choose fields of study based on ", html.B("personal interest"), " rather than ", html.B("economic necessity"), ". As a result, many turn toward non-STEM disciplines, such as languages or the humanities. By contrast, in emerging countries like Algeria or Tunisia, STEM fields are widely perceived as ", html.B("reliable pathways"), " to social mobility and financial stability, making them more attractive to women despite persistent gender inequalities."])
                    ),
                    html.Img(
                        src="/assets/images/sign_gender.png",
                        className="icon_3d big",
                        alt="politic 3d icon"
                    ),
                ]
            ),
            create_card(
                html.H3(
                    className="h3_normal",
                    children=[
                        html.P("In short, we are confronted with a double reality. In very poor countries, women are systematically excluded due to economic constraints and deeply rooted social norms. At the same time, the Gender Equality Paradox shows that even when barriers related to wealth and formal equality are removed, stereotypes continue to discourage women from pursuing STEM careers. Today, the challenge remains the same across contexts: encouraging women to break free from stereotypes and become active agents of innovation.")
                    ]
                )
            )
        ]
    )