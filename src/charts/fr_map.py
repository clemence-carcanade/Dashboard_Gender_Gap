import pandas as pd
from dash import html, dcc
from config import COLORSCALE_BLUE, COLORSCALE_PINK
from src.utils.get_data import get_fr_departments_data, get_fr_geojson
from src.utils.chart import create_france_choropleth

df_departments = get_fr_departments_data()
france_geojson = get_fr_geojson()

df_departments['Code'] = df_departments['Code'].str.zfill(2)

real_min_edu = df_departments["Education_Gap_2021"].min(skipna=True)
real_min_sal = df_departments["Salary_Gap_2022_abs"].min(skipna=True)

sentinel_edu = real_min_edu - (abs(real_min_edu) * 0.1 + 0.01)
sentinel_sal = real_min_sal - (abs(real_min_sal) * 0.1 + 0.01)

df_departments["Education_Gap_plot"] = df_departments["Education_Gap_2021"].fillna(sentinel_edu)
df_departments["Salary_Gap_plot"] = df_departments["Salary_Gap_2022_abs"].fillna(sentinel_sal)

df_departments["Education_Gap_hover"] = df_departments["Education_Gap_2021"].apply(
    lambda x: x if pd.notna(x) else "Unknown"
)
df_departments["Salary_Gap_hover"] = df_departments["Salary_Gap_2022_abs"].apply(
    lambda x: x if pd.notna(x) else "Unknown"
)

def education_map_layout(metric):
    if metric == "Disparity in Education":
        color_col = "Education_Gap_plot"
        hover_col = "Education_Gap_hover"
        subtitle_text = "Women exceeding Men in Higher Education (%)"
        colorscale = COLORSCALE_PINK
        z_min = df_departments[color_col].min()
        z_max = df_departments["Education_Gap_2021"].max()
        hover_template = '<b>%{customdata[0]}</b><br>Education Gap: %{customdata[1]}<extra></extra>'
        colorbar_title = "Gap in<br>Education (%)"
    else:  # "Wage Inequality"
        color_col = "Salary_Gap_plot"
        hover_col = "Salary_Gap_hover"
        subtitle_text = "Difference in Wage between Women and Men (%)"
        colorscale = COLORSCALE_BLUE
        z_min = df_departments[color_col].min()
        z_max = df_departments["Salary_Gap_2022_abs"].max()
        hover_template = '<b>%{customdata[0]}</b><br>Wage Gap (%): %{z:.1f}<extra></extra>'
        colorbar_title = "Gap in<br>Wage (%)"
    
    fig = create_france_choropleth(
        df=df_departments,
        geojson=france_geojson,
        locations_col="Code",
        color_col=color_col,
        colorscale=colorscale,
        range_color=(z_min, z_max),
        colorbar_title=colorbar_title,
        subtitle_text=subtitle_text,
        hover_template=hover_template,
        custom_data=['Region', hover_col],
    )
    
    return html.Div(
        className="data_container",
        children=[
            dcc.Graph(
                figure=fig,
                config={"displayModeBar": False, "responsive": True}
            )
        ]
    )