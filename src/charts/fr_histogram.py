from dash import html, dcc
from config import COLORSCALE_BLUE, COLORSCALE_PINK
from src.utils.get_data import get_fr_departments_data, add_bins_to_dataframe
from src.utils.chart import create_histogram_by_range

df_departments = get_fr_departments_data()
df_departments = df_departments.dropna(subset=['Education_Gap_2021'])

bins = [0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5]
labels = ['0-2.5%', '2.5-5%', '5-7.5%', '7.5-10%', '10-12.5%', 
          '12.5-15%', '15-17.5%', '17.5-20%', '20-22.5%']

df_departments = add_bins_to_dataframe(df_departments, 'Education_Gap_2021', bins, labels)
df_departments = add_bins_to_dataframe(df_departments, 'Salary_Gap_2022_abs', bins, labels)

def education_bars_layout(metric):
    fig = create_bar_figure(metric)

    return html.Div(
        className="data_container",
        children=[
            dcc.Graph(
                figure=fig,
                config={"displayModeBar": False, "responsive": True}
            )
        ]
    )

def create_bar_figure(selected_metric):
    if selected_metric == "Disparity in Education":
        fig = create_histogram_by_range(
            df=df_departments,
            range_column='Education_Gap_2021_Range',
            colorscale=COLORSCALE_PINK,
            xlabel="Women exceeding Men in Higher Education (%)",
            ylabel="Departments number",
        )
    else:  # Wage Inequality
        fig = create_histogram_by_range(
            df=df_departments,
            range_column='Salary_Gap_2022_abs_Range',
            colorscale=COLORSCALE_BLUE,
            xlabel="Difference in Wage between Women and Men (%)",
            ylabel="Departments number",
        )
    
    return fig