import plotly.express as px
from dash import Input, Output, html, dcc, callback
import pandas as pd
from src.charts.slider import create_slider
from src.components.segmented_control import create_segmented_control

df = pd.read_csv("data/raw/world_GII.csv")

gii_columns = [col for col in df.columns if col.startswith("Gender Inequality Index")]

df_long = df.melt(
    id_vars=["ISO3", "Country", "Continent"],
    value_vars=gii_columns,
    var_name="Year",
    value_name="GII"
)

df_long['Year'] = df_long['Year'].str.extract(r'(\d{4})').astype(int)
df_long = df_long.dropna(subset=['GII'])
years = sorted(df_long["Year"].unique())
continent = ["All"] + sorted(df_long["Continent"].dropna().unique())

colorscale = [
    [0.0, "#EDEDED"],
    [0.00001, "#FBEAF4"],
    [0.1, "#F4C3E0"],
    [0.2, "#EDA1CE"],
    [0.3, "#E576B8"],
    [0.4, "#DE4FA5"],
    [0.5, "#D62991"],
    [0.6, "#B02177"],
    [0.7, "#891A5D"],
    [1.0, "#631343"],
]

zmin = df_long["GII"].min()
zmax = df_long["GII"].max()

def layout():
    return html.Div(
        className="world_data_container",
        children=[
            create_segmented_control(
                className="segmented_control small middle",
                id="continent_selector",
                options=continent,
            ),
            dcc.Graph(
                id='gii_histogram',
                config={
                    "displayModeBar": False,
                    "responsive": True
                }
            ),
            create_slider(years, slider_id="gii_histogram"),
        ])

@callback(
    Output('gii_histogram', 'figure'),
    [Input({"type": "year-slider", "id": "gii_histogram"}, "value"),
     Input('continent_selector', 'value')]
)
def update_map(selected_year, selected_continent):
    df_filtre = df_long[df_long["Year"] == selected_year].copy()
    
    if selected_continent != "All":
        df_filtre = df_filtre[df_filtre["Continent"] == selected_continent]
        df_filtre["Country_short"] = df_filtre["Country"].str.slice(0, 8)
        x_col = 'Country_short'
    else:
        x_col = 'Country'
    
    fig = px.bar(
        df_filtre,
        x=x_col,
        y='GII',
        labels={'GII': 'GII', "Country": 'Countries', "Country_short": "Countries"},
        color='GII',
        color_continuous_scale=colorscale,
        hover_data={
            "Country": True,
            "GII": True,
            x_col: False
        },
        range_color=(zmin, zmax),
        custom_data=['Country']
    )
    
    fig.update_traces(
        hovertemplate='<b>%{customdata[0]}</b><br>GII: %{y}<extra></extra>'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        yaxis=dict(range=[0, zmax]),
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_colorbar=dict(len=1.5),
        font=dict(family="SF Pro Display"),
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#DDDDDD",
    )
    
    if selected_continent == "All":
        fig.update_xaxes(
            showticklabels=False,
            title="Countries"
        )
    else:
        fig.update_xaxes(title=None)
    
    return fig