from dash import html
from src.components.card import create_card

def layout():
    return html.Div(
        className="world_analysis_written",
        children=[
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--pink)",
                    "--top": "5100px",
                    "--left": "50px"
                }
            ),
            html.Div(
                className="background-glow",
                style={
                    "--color": "var(--pink)",
                    "--top": "5600px",
                    "--right": "250px"
                }
            ),
            html.Div(
                className="illustrated_text",
                children=[
                    create_card(
                        html.P(["To conclude our analysis, we examined how women’s participation in scientific fields in France has evolved over the past decade. The overall picture reveals remarkable ", html.B("stability rather than progress"), ". Women remain highly concentrated in life sciences and healthcare-related fields, where they represent a clear majority of students, while continuing to be significantly underrepresented in technological and theoretical disciplines."]),
                        html.P(["Engineering illustrates this imbalance particularly well. Although women account for close to 50% of students overall, this apparent progress conceals strong ", html.B("internal disparities"), ". Fields related to biology or agri-food, where women are well represented, compensate for sectors such as computer science and mechanics, where female participation often remains very low. As a result, aggregate figures tend to mask the persistence of gender segregation within engineering."]),
                    ),
                    html.Img(
                        src="/assets/images/biology.png",
                        className="icon_3d",
                        alt="biology 3d icon"
                    ),
                ]
            ),
            create_card(
                html.H3(
                    className="h3_normal",
                    children=[
                        html.P("This divide raises a fundamental question: why do women continue to gravitate toward life sciences while remaining marginalised in technological and theoretical fields?")
                    ]
                )
            ),
            html.Div(
                className="illustrated_text",
                children=[
                    html.Img(
                        src="/assets/images/engineering.png",
                        className="icon_3d",
                        alt="engineering 3d icon"
                    ),
                    create_card(
                        html.P(["Part of the answer lies in early socialisation. From childhood onward, girls are more often encouraged to develop ", html.B("interpersonal and caring skills"), ", while boys are steered toward activities associated with logic and technical mastery. These gendered expectations shape educational choices over time. The lack of visible ", html.B("female role models"), " in fields such as engineering and computer science further limits girls’ ability to imagine themselves in these careers. This is reinforced by ", html.B("self-censorship"), ": when women are a minority in a field, they are less likely to feel legitimate or confident in pursuing it, particularly in contexts where stereotypes about aptitude persist."]),
                        html.P(["These patterns are already visible at the doctoral level. Women are more likely to pursue humanities, social sciences, and biology, while remaining a minority in mathematics, computer science, and engineering. Crucially, these distributions have changed very little over the past ten years, suggesting that gendered orientations in science are ", html.B("deeply entrenched rather than transitional.")])
                    ),
                ]
            ),
            create_card(
                html.H3(
                    className="h3_normal",
                    children=[
                        html.P("Our findings reveal a stagnation in women’s representation in science in France. Despite increased awareness and policy efforts, women remain concentrated in life sciences and underrepresented in “hard sciences.” This divide reflects not individual choice alone, but enduring stereotypes and a lack of role models that continue to limit women’s participation. The challenge, therefore, is not only to expand access, but to create scientific environments in which women truly feel they belong.")
                    ]
                )
            ),
        ]
    )