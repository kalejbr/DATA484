# /////////////////////////////////////////////////////////////////////////////////
# ///           University of Hawaii
# /// @brief   Project1 - DATA 484 - Fall 2022
# ///
# ///
# /// @version 1.0 - Creates a dashboard using Plotly and Dash
# ///       Reads in csv files from data folder containing
# ///       cholera data. Generates 4 data visualizations and
# ///       includes reference information.
# ///
# /// @author  Kale Beever-Riordon <kalejbr@hawaii.edu>
# /// @date    08_SEP_2022
# ///
# /// @see     https://plotly.com/python-api-reference/
# ///          https://dash.plotly.com
# ///
# ///////////////////////////////////////////////////////////////////////////////

# Import required libraries
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.colors import n_colors
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import random
import warnings

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Initialize the Dash app layout, creates a container with 5 tabs
app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("DATA 484 - Project 1"),
        html.Hr(),

        dbc.Tabs(
            [
                dbc.Tab(label='UK Census - 1851', tab_id='tab-1'),
                dbc.Tab(label='UK Cholera Outbreak', tab_id='tab-2'),
                dbc.Tab(label='Cholera - Naples, IT', tab_id='tab-3'),
                dbc.Tab(label='UK Cholera ScatterMap', tab_id='tab-4'),
                dbc.Tab(label='References', tab_id='tab-5'),
            ],
            id="tabs",
            active_tab="Tab one",
        ),
        html.Div(className="p-1", id='tabs-example-content-1'),
    ]
)


#
@app.callback(
    Output('tabs-example-content-1', 'children'),
    Input('tabs', 'active_tab')
)
def update_output(fig_name):
    return name_to_figure(fig_name)


# Input from the selected tab is passed and a figure is generated accordingly
def name_to_figure(active_tab):

    if active_tab == 'tab-1':
        fig = go.Figure()

        def format_df(dataframe):
            dataframe.loc[:, "male"] = dataframe["male"].map('{:,d}'.format)
            dataframe.loc[:, "female"] = dataframe["female"].map('{:,d}'.format)
            dataframe.loc[:, "all"] = dataframe["all"].map('{:,d}'.format)
            return dataframe

        # Import and copy data: df2 is used to display formatted values
        df = pd.read_csv('data/UKcensus1851.csv', header=2)
        df2 = pd.read_csv('data/UKcensus1851.csv', header=2)
        new_row = pd.DataFrame({'age': 'Total', 'male': df['male'].sum(), 'female': df['female'].sum()},
                               index=[len(df)])
        df = pd.concat([new_row, df.loc[:]]).sort_index()
        df2 = pd.concat([new_row, df2.loc[:]]).sort_index()
        df['all'] = df['male'] + df['female']
        df2['all'] = df2['male'] + df2['female']
        format_df(df2)

        datum = ['male', 'female']

        fig = make_subplots(rows=3, cols=2,
                            vertical_spacing=0.05,
                            specs=[[{"type": "table"}, {"type": "pie"}],
                                   [{"type": "pie"}, {"type": "pie"}],
                                   [{"colspan": 2}, {"type": "bar"}]])
        fig.add_trace(
            go.Table(
                header=dict(
                    values=["Age", "Male", "Female", "All"],
                    font=dict(
                        color='rgb(247, 246, 246)',
                        size=17,
                        family="Roboto"
                    ),
                    fill_color='#2b2b2b',
                    line_color="#2b2b2b",
                    align="center",
                    height=26
                ),
                cells=dict(
                    values=[df2[xy].tolist() for xy in df2.columns[0:]],
                    # line_color=[np.array(colors)[arr1], np.array(colors)[arr2]],
                    line_color="#1f1e1e",
                    fill_color="rgb(3, 3, 3)",
                    font_color="rgb(201, 202, 204)",
                    align=('left','right'),
                    height=22,
                )
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Pie(
                values=[df.loc[len(df) - 1, 'male'], df.loc[len(df) - 1, 'female']],
                labels=["male", "female"],
                hoverinfo="value+label",
                title=dict(
                    text="Population according to UK census",
                    font=dict(
                        size=18,
                        color="rgb(201, 202, 204)"
                    )
                ),
                marker=dict(
                    colors=[
                        "#5e7bd1",
                        "#db0763"
                    ]
                ),
                domain=dict(x=[0.5, 1.0])
            ),
            row=2, col=1
        )

        df = df.drop(df.index[-1])
        fig.add_trace(
            go.Pie(
                hole=0.4,
                values=df['male'],
                labels=df['age'],
                title=dict(
                    text="UK Males <br>by Age",
                    font=dict(
                        size=18,
                        color="rgb(255,255,255)")
                ),

                domain=dict(x=[0, 0.5]),
                marker=dict(
                    colors=[
                        "#f7fcfd",
                        "#e0ecf4",
                        "#bfd3e6",
                        "#9ebcda",
                        "#8c96c6",
                        "#8c6bb1",
                        "#88419d",
                        "#810f7c",
                        "#4d004b"
                    ]
                ),
                textinfo="percent",
                hoverinfo="value+label",
                insidetextfont=dict(
                    color="rgb(0, 0, 0)",
                    size=18,
                    family="Arial"
                ),
                outsidetextfont=dict(
                    color="rgb(255, 255, 255)",
                    size=14,
                    family="Arial"
                ),
            ),
            row=1, col=2
        )

        fig.add_trace(
            go.Pie(
                hole=0.4,
                values=df['female'],
                labels=df['age'],
                title=dict(
                    text="UK Females <br>by Age",
                    font=dict(
                        size=18,
                        color="rgb(255, 255, 255)")
                ),
                domain=dict(x=[0.5, 1.0]),
                marker=dict(
                    colors=[
                        "#f7f4f9",
                        "#e7e1ef",
                        "#d4b9da",
                        "#c994c7",
                        "#df65b0",
                        "#e7298a",
                        "#ce1256",
                        "#980043",
                        "#67001f"
                    ]
                ),
                textinfo="percent",
                hoverinfo="value+label",
                insidetextfont=dict(
                    color="rgb(0, 0, 0)",
                    size=18,
                    family="Arial"
                ),
                outsidetextfont=dict(
                    color="rgb(255, 255, 255)",
                    size=14,
                    family="Arial"
                ),
            ),
            row=2, col=2
        )

        fig.add_trace(
            trace=go.Bar(
                x=df['age'],
                y=df[datum[0]],
                name=datum[0],
                marker=dict(
                    color="#5e7bd1",
                    # color= df[datum[0]],
                    # cmin=-2000000,
                    # cmax=3000000,
                    # colorscale='bupu',
                    line=dict(
                        color="#d95604",
                        # color= df[datum[0]],
                        # colorscale='inferno',
                        width=1
                    )
                ),
            ),
            row=3, col=1
        )

        fig.add_trace(
            trace=go.Bar(
                x=df['age'],
                y=df[datum[1]],
                name=datum[1],
                marker=dict(
                    color="#db0763",
                    # color=df[datum[1]],
                    # cmin=-2000000,
                    # cmax=3000000,
                    # colorscale="purd",
                    line=dict(
                        color="#d95604",
                        # color=df[datum[0]],
                        # colorscale='inferno',
                        width=1
                    )
                ),
            ),
            row=3, col=1
        )

        fig.update_layout(
            # annotations=[dict(),],
            height=1100,
            # width=1400,
            showlegend=False,
            title=dict(
                text='UK Census 1851',
                x=0.5,
                font=dict(
                    size=22,
                    color="rgb(247, 246, 246)",
                    family="Roboto"
                )
            ),
            paper_bgcolor="rgb(3, 3, 3)",
            plot_bgcolor="rgb(3, 3, 3)",
            xaxis=dict(
                title='Age Range',
                titlefont_color="rgb(201, 202, 204)",
                titlefont_size=18,
                tickfont_color="rgb(201, 202, 204)",
                tickfont_size=14,
                tickangle=-15
            ),
            yaxis=dict(
                title='# of People',
                titlefont_color="rgb(201, 202, 204)",
                titlefont_size=18,
                tickfont_color="rgb(201, 202, 204)",
                tickfont_size=14,
                zerolinewidth=0,
                gridcolor="#a2a2a2"
            )
        )
        return html.Div([

            dcc.Graph(
                figure=fig
            )
        ])

    elif active_tab == 'tab-2':
        df = pd.read_table('data/choleraDeaths.tsv')
        cols = ["Today's Attacks", 'Total Attacks', "Today's Deaths", 'Total Deaths']

        df['Date'] = pd.to_datetime(df['Date'])
        df['Date'] = df['Date'].dt.date

        data = []

        for col in cols:
            trace = go.Scatter(
                x=df.Date[:1],
                y=df[col][:1],
                mode='lines',
                name=col,
            )
            data.append(trace)

        layout = go.Layout(
            # autosize=True,
            # width=1440,
            height=600,
            showlegend=False,
            updatemenus=[dict(type='buttons', showactive=False,
                              y=1.05,
                              x=1.15,
                              xanchor='right',
                              yanchor='top',
                              pad=dict(t=0, r=10),
                              buttons=[dict(label="Play",
                                            method='animate',
                                            args=[None,
                                                  dict(frame=dict(duration=70,
                                                                  redraw=False),
                                                       transition=dict(duration=0),
                                                       fromcurrent=False,
                                                       mode='immediate')])])])

        layout.update(xaxis=(dict(range=[df.Date[0], df.Date[len(df) - 1]],
                                  autorange=False,
                                  nticks=18,
                                  tickangle=45,
                                  tickson="labels",
                                  tickfont={
                                      "size": 20,
                                      "color": "rgb(213, 213, 214)"
                                  },
                                  gridcolor="rgb(55, 66, 82)",
                                  gridwidth=0,
                                  zerolinewidth=0,
                                  zerolinecolor="rgb(70, 114, 138)"
                                  )
                             ),
                      yaxis=dict(range=[min(df['Total Attacks'] - 10), max(df['Total Deaths'] + 50)],
                                 autorange=False,
                                 zerolinewidth=0,
                                 zerolinecolor="rgb(55, 66, 82)",
                                 type="linear",
                                 title=dict(
                                     text="# of Individuals",
                                     font={
                                         "size": 24
                                     }
                                 ),
                                 tickson='boundaries',
                                 gridwidth=0,
                                 gridcolor="rgb(34, 41, 51)",
                                 tickfont={
                                     "size": 20,
                                     "color": "rgb(213, 213, 214)"
                                 },
                                 ),
                      margin={
                          "t": 100,
                          "l": 150,
                          "b": 100,
                          "pad": 30
                      },
                      # hovermode='x unified',
                      hoverlabel=dict(namelength=-1, font_size=18, ),
                      paper_bgcolor="rgb(17,17,17)",
                      plot_bgcolor="rgb(17,17,17)",
                      font={
                          "color": "rgb(247, 246, 246)",
                          "family": "Roboto"
                      },
                      title=go.layout.Title(
                          x=0.48,
                          text='Cholera Outbreak - London 1854',
                          font={
                              "color": "rgb(247, 246, 246)",
                              "family": "Roboto"
                          },
                      ),
                      )

        frames = [dict(data=[dict(type='scatter',
                                  x=df.Date[:k + 1],
                                  y=df[cols[0]][:k + 1]),
                             dict(type='scatter',
                                  x=df.Date[:k + 1],
                                  y=df[cols[1]][:k + 1]),
                             dict(type='scatter',
                                  x=df.Date[:k + 1],
                                  y=df[cols[2]][:k + 1]),
                             dict(type='scatter',
                                  x=df.Date[:k + 1],
                                  y=df[cols[3]][:k + 1])],
                       ) for k in range(1, len(df[cols[0]] - 1))]

        fig = go.Figure(data=data, frames=frames, layout=layout)
        fig.update_layout(hovermode='x')
        return html.Div([

            dcc.Graph(
                figure=fig
            )
        ])
    elif active_tab == 'tab-3':
        colors = n_colors('rgb(252, 211, 182)', 'rgb(250, 105, 2)', 40, colortype='rgb')

        df = pd.read_table('data/naplesCholeraAgeSexData.tsv', header=6)
        # print(df)

        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.13,
            specs=[
                [{"type": "bar"}],
                [{"type": "table"}]
                ]
        )

        fig.add_trace(
            go.Table(
                header=dict(
                    values=["Age", "Male", "Female"],
                    font=dict(
                        color='rgb(247, 246, 246)',
                        size=17,
                        family="Roboto"
                    ),
                    fill_color='#2b2b2b',
                    line_color="#2b2b2b",
                    align="center",
                    height=27
                ),
                cells=dict(
                    values=[df[xy].tolist() for xy in df.columns[0:]],
                    line_color=[np.array(colors)[df['male'].to_numpy(int)],
                                np.array(colors)[df['female'].to_numpy(int)]],
                    fill_color=[np.array(colors)[df['male'].to_numpy(int)],
                                np.array(colors)[df['female'].to_numpy(int)]],
                    align='center')
            ),
            row=2, col=1
        )

        fig.add_trace(
            trace=go.Bar(
                x=df['age'],
                y=df['male'],
                name='Male',
                marker=dict(
                    color="#5e7bd1",
                    # color= df[datum[0]],
                    # cmin=-2000000,
                    # cmax=3000000,
                    # colorscale='bupu',
                    line=dict(
                        color="#d95604",
                        # color= df[datum[0]],
                        # colorscale='inferno',
                        width=1
                    )
                )
            ),
            row=1, col=1
        )

        fig.add_trace(
            trace=go.Bar(
                x=df['age'],
                y=df['female'],
                name='Female',
                marker=dict(
                    color="#db0763",
                    # color=df[datum[1]],
                    # cmin=-2000000,
                    # cmax=3000000,
                    # colorscale="purd",
                    line=dict(
                        color="#d95604",
                        # color=df[datum[0]],
                        # colorscale='inferno',
                        width=1
                    )
                )
            ),
            row=1, col=1
        )

        fig.update_layout(
            height=900,
            showlegend=False,
            title=dict(
                text='Cholera in Naples',
                x=0.5,
                font=dict(
                    size=22,
                    color="rgb(247, 246, 246)",
                    family="Roboto"
                )
            ),
            paper_bgcolor="rgb(3, 3, 3)",
            plot_bgcolor="rgb(3, 3, 3)",
            xaxis=dict(
                title='Age Range',
                titlefont_color="rgb(201, 202, 204)",
                titlefont_size=18,
                tickfont_color="rgb(201, 202, 204)",
                tickfont_size=14,
                tickangle=-15
            ),
            yaxis=dict(
                title='Deaths per 10,000',
                titlefont_color="rgb(201, 202, 204)",
                titlefont_size=18,
                tickfont_color="rgb(201, 202, 204)",
                tickfont_size=14,
                zerolinewidth=0,
                gridcolor="#a2a2a2"
            )
        )
        return html.Div([

            dcc.Graph(
                figure=fig
            )
        ])
    if active_tab == 'tab-4':
        warnings.filterwarnings("ignore")

        df = pd.read_csv('data/choleraDeathLocations.csv')
        df2 = pd.read_csv('data/choleraPumpLocations.csv')
        lat1 = df.Lat
        lon1 = df.Lon
        lat2 = df2.Lt
        lon2 = df2.Ln

        random.Random(3).shuffle(lat1)
        random.Random(3).shuffle(lon1)
        random.Random(3).shuffle(df['Deaths'])

        fig = go.Figure()

        fig.add_trace(
            go.Scattermapbox(
                lat=lat1[:1],
                lon=lon1[:1],
                mode='markers',
                marker=dict(
                    color = df['Deaths'],
                    colorscale='Agsunset',
                ),
                name='Casualty Location',
                hovertemplate=
                '<b>Reported Deaths: </b>%{text}<extra></extra>' +
                '<br>\u03D1: %{lat}' +
                '<br>\u03D5: %{lon}',
                text=df["Deaths"].values.tolist(),
                hoverinfo="text+lat+lon"
            )
        )
        fig.add_trace(
            go.Scattermapbox(
                lat=lat2,
                lon=lon2,
                mode='markers',
                marker=dict(
                    size=8,
                    color='rgb(255, 72, 0)'
                ),
                name="Pump Location",
                hovertemplate='<b>Pump No: </b>%{text}<extra></extra>',
                text=df2["Pump No."].values.tolist(),
                hoverinfo="text+lat+lon",
            )
        )

        fig.update_layout(
            # autosize=True,
            height=600,
            legend=dict(
                yanchor='top',
                y=0.99,
                xanchor='left',
                x=0.01,
                font=dict(
                    family='Arial',
                    size=12,
                    color='white'
                ),
            ),
            title=dict(
                text='UK Cholera Outbreak',
                x=0.5,
                font=dict(
                    size=22,
                    color="rgb(247, 246, 246)",
                    family="Roboto"
                )
            ),
            hovermode='closest',
            mapbox=dict(
                style='carto-darkmatter',
                bearing=64,
                center=go.layout.mapbox.Center(
                    lat=51.51337173947445,
                    lon=-0.13686837809898589
                ),
                pitch=60,
                zoom=16.182448580347329
            ),
            yaxis=dict(
                range=[
                    -0.14062545007800312,
                    -0.13238154992199688
                ],
                autorange=True
            ),
            xaxis=dict(
                range=[
                    51.511608752969124,
                    51.516081247030876
                ],
                autorange=True
            ),
            paper_bgcolor="rgb(0,0,0)"
        )

        frames = [dict(data=[dict(type='scattermapbox',
                                  lat=df.loc[:k + 1, 'Lat'],
                                  lon=df.loc[:k + 1, 'Lon']
                                  )],
                       traces=[0],
                       name=f'frame{k}'
                       ) for k in range(len(df))]

        fig.update(frames=frames)

        sliders = [dict(steps=[dict(method='animate', args=[[f'frame{k}'],
                                                            dict(mode='immediate',
                                                                 frame=dict(duration=100, redraw=True),
                                                                 transition=dict(duration=0))
                                                            ],
                                    label='{:d}'.format(k))
                               for k in range(len(df))],
                        transition=dict(duration=0),
                        x=0,
                        y=0,
                        currentvalue=dict(font=dict(size=12),
                                          prefix='Point: ',
                                          visible=True,
                                          xanchor='center'),
                        len=1.0)
                   ]

        fig.update_layout(updatemenus=[dict(type='buttons', showactive=False,
                                            y=0,
                                            x=1.05,
                                            xanchor='right',
                                            yanchor='top',
                                            pad=dict(t=0, r=10),
                                            buttons=[dict(label='Play',
                                                          method='animate',
                                                          args=[None,
                                                                dict(frame=dict(duration=200,
                                                                                redraw=True),
                                                                     transition=dict(duration=0),
                                                                     fromcurrent=True,
                                                                     mode='immediate')
                                                                ]
                                                          )
                                                     ]
                                            )
                                       ],
                          sliders=sliders)
        return html.Div([

            dcc.Graph(
                figure=fig
            )
        ])
    if active_tab == 'tab-5':
        return html.Div([
            html.H4('Project Information'),
            dcc.Markdown("""By: Kale Beever-Riordon\
            """),

            dcc.Markdown("""
            
            About the Project: \
            
            """),

            dcc.Markdown("""
            
            &nbsp;&nbsp;&nbsp;&nbsp;Libraries used: Plotly, Dash, Pandas, Numpy, and Dash Bootstrap Components\
             
             """),
            dcc.Markdown("""&nbsp;&nbsp;&nbsp;&nbsp;Data used: Derived from Jon Snow's works during the 3rd great Cholera \
            
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Outbreak in London. It includes the locations of casualties from the outbreak, the\
            
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;locations of 6 water pumps in the SoHo neighborhood, the Census numbers from\
            
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1851, and information regarding a cholera outbreak in Naples, Italy.\
            
            """),

            dcc.Markdown("""
            
            [Project Github](https://github.com/kalejbr/DATA484)
 
            """)

        ])


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
