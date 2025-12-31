import plotly.express as px
import dash
from dash import Dash, Input, Output, html, dcc

#
# Data
#

year = 2002

gapminder = px.data.gapminder() # (1)
years = gapminder["year"].unique()
data = { year:gapminder.query("year == @year") for year in years} # (2)

#
# Main
#

if __name__ == '__main__':

    app = dash.Dash(__name__) # (3)

    fig = px.scatter(data[year], x="gdpPercap", y="lifeExp",
                        color="continent",
                        size="pop",
                        hover_name="country") # (4)
    app.layout = html.Div(children=[

                            html.Label('Year'),
                            dcc.Interval(   id='interval',
                            interval=1*1000, # in milliseconds
                            n_intervals=0,
                            disabled=True),
                            dcc.Slider(id="year-dropdown",
                                     min=int(years.min()),
                                       max=int(years.max()),
                                       step=1,
                               marks={int(y): str(y) for y in years},
                               value=year),
                            html.H1(id='titre', children=f'Life expectancy vs GDP per capita ({year})',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

                            dcc.Graph(
                                id='graph1',
                                figure=fig
                            ), # (6)

                           html.Div(
                                children=[
                                    html.Button('PLAY', id='btn-nclicks-1', n_clicks=0),
                                    html.Button('PAUSE', id='btn-nclicks-2', n_clicks=0),
                                    html.Div(
                                        id='legende',
                                        children=f'''
                                        The graph above shows relationship between life expectancy and
                                        GDP per capita for year {year}. Each continent data has its own
                                        colour and symbol size is proportionnal to country population.
                                        Mouse over for details.
                                        '''
                                    )
                                ]
                            ),
    ])
    @app.callback(  [Output('year-dropdown', 'value'),Output('interval', 'disabled')],
                [Input('interval', 'n_intervals'), Input('btn-nclicks-1', 'n_clicks'),  # bouton PLAY
     Input('btn-nclicks-2', 'n_clicks')])
    def on_tick(n_intervals, play_clicks, pause_clicks):
        if play_clicks == 0 and pause_clicks == 0:
            return year, True
        if pause_clicks > play_clicks:
            return dash.no_update, True
        if play_clicks > pause_clicks:
            new_year = int(years[(n_intervals + 1) % len(years)])
            return new_year, False
        return dash.no_update, dash.no_update
    @app.callback(
    [Output(component_id='graph1', component_property='figure'),
    Output(component_id='titre', component_property='children'),
    Output(component_id='legende', component_property='children')], # (1)
    [Input(component_id='year-dropdown', component_property='value')] )# (2)

    def update_figure(input_value): # (3)
        fig=px.scatter(data[input_value], x="gdpPercap", y="lifeExp",
                        color="continent",
                        size="pop",
                        hover_name="country")
        titre=f'Life expectancy vs GDP per capita ({input_value})'
        legende=f'''
                                The graph above shows relationship between life expectancy and
                                GDP per capita for year {input_value}. Each continent data has its own
                                colour and symbol size is proportionnal to country population.
                                Mouse over for details.
                            '''
        return  (fig,titre,legende)


    
    #
    # RUN APP
    #

    app.run(debug=True)