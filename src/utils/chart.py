import plotly.express as px

def apply_common_layout(fig, font_family="SF Pro Display", font_size=14):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family=font_family, size=font_size),
        showlegend=False,
    )
    return fig


def apply_grid_style(fig, show_xgrid=False, show_ygrid=True, gridcolor="#DDDDDD"):
    fig.update_xaxes(showgrid=show_xgrid, gridcolor=gridcolor)
    fig.update_yaxes(showgrid=show_ygrid, gridcolor=gridcolor)
    return fig

def create_bar_chart(
    df,
    x,
    y,
    color_col,
    colorscale,
    labels,
    hover_template,
    xaxis_title=None,
    yaxis_title=None,
    height=None,
    range_color=None,
    xaxis_angle=-45,
    custom_data=None
):
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color_col,
        color_continuous_scale=colorscale,
        labels=labels,
        custom_data=custom_data,
        range_color=range_color,
    )
    
    fig.update_traces(hovertemplate=hover_template)
    
    layout_kwargs = {
        "xaxis_tickangle": xaxis_angle,
        "coloraxis_showscale": False,
    }
    
    if xaxis_title:
        layout_kwargs["xaxis_title"] = xaxis_title
    if yaxis_title:
        layout_kwargs["yaxis_title"] = yaxis_title
    if height:
        layout_kwargs["height"] = height
    
    fig.update_layout(**layout_kwargs)
    
    apply_common_layout(fig)
    apply_grid_style(fig)
    
    return fig


def create_histogram_by_range(
    df,
    range_column,
    colorscale,
    xlabel,
    ylabel="Departments number",
    hover_template='<b>%{x}</b><br>Departments: %{y}<extra></extra>'
):
    counts = (
        df
        .groupby(range_column, observed=False)
        .size()
        .reset_index(name='count')
    )
    
    fig = px.bar(
        counts,
        x=range_column,
        y='count',
        labels={
            range_column: xlabel,
            'count': ylabel
        },
        color='count',
        color_continuous_scale=colorscale
    )
    
    fig.update_traces(hovertemplate=hover_template)
    fig.update_layout(yaxis_title=ylabel, coloraxis_showscale=False)
    
    apply_common_layout(fig)
    apply_grid_style(fig)
    
    return fig

def create_world_choropleth(
    df,
    geojson,
    locations_col,
    color_col,
    hover_name_col,
    hover_data_cols,
    featureidkey,
    colorscale,
    range_color,
    colorbar_title,
    hover_template,
    projection="natural earth",
    marker_line_color="#DDDDDD",
    marker_line_width=0.9,
):
    fig = px.choropleth(
        df,
        geojson=geojson,
        locations=locations_col,
        color=color_col,
        hover_name=hover_name_col,
        hover_data=hover_data_cols,
        featureidkey=featureidkey,
        projection=projection,
        color_continuous_scale=colorscale,
        range_color=range_color,
    )
    
    fig.update_traces(
        marker_line_color=marker_line_color,
        marker_line_width=marker_line_width,
        hovertemplate=hover_template
    )
    
    fig.update_geos(fitbounds="locations", visible=False)
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(
            title=colorbar_title,
            thickness=30,
            len=0.95,
            y=0.5,
            bgcolor="rgba(255,255,255,0.8)",
            tickfont=dict(family="SF Pro Display", size=11),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="SF Pro Display"),
    )
    
    return fig


def create_france_choropleth(
    df,
    geojson,
    locations_col,
    color_col,
    colorscale,
    range_color,
    colorbar_title,
    subtitle_text,
    hover_template,
    custom_data,
):
    fig = px.choropleth(
        df,
        geojson=geojson,
        locations=locations_col,
        color=color_col,
        featureidkey="properties.code",
        color_continuous_scale=colorscale,
        range_color=range_color,
        custom_data=custom_data
    )
    
    fig.update_traces(
        marker_line_color="#DDDDDD",
        marker_line_width=0.9,
        hovertemplate=hover_template
    )
    
    fig.update_geos(fitbounds="locations", visible=False)
    
    fig.update_layout(
        annotations=[
            dict(
                text=subtitle_text,
                x=0.55,
                y=-0,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(family="SF Pro Display", size=18, color="#333333")
            )
        ],
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(
            title=colorbar_title,
            thickness=30,
            len=0.95,
            y=0.5,
            bgcolor="rgba(255,255,255,0.8)",
            tickfont=dict(family="SF Pro Display", size=11),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="SF Pro Display"),
        geo=dict(
            projection_type="mercator",
            center=dict(lat=46.5, lon=2.5),
            projection_scale=15
        )
    )
    
    return fig

def update_projection(fig, projection_type):
    fig.update_geos(projection_type=projection_type)
    return fig