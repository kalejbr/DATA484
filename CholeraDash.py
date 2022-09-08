import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import pandas as pd


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Dynamically rendered tab content"),
        html.Hr(),

        dbc.Tabs(
            [
                dbc.Tab(label='Tab one', tab_id='tab-1'),
                dbc.Tab(label='Tab two', tab_id='tab-2'),
            ],
            id="tabs",
            active_tab="Tab one",
        ),
        html.Div(className="p-1", id='tabs-example-content-1'),
    ]
)


# app.layout = html.Div(children=[
#     dcc.Tabs(style=tabs_styles, id='tabs-example-1', value='tab-1', children=[
#         dcc.Tab(label='Tab one', value='tab-1', style=tab_style,
#                  selected_style=tab_selected_style),
#         dcc.Tab(label='Tab two', value='tab-2', style=tab_style,
#                  selected_style=tab_selected_style),
#     ], className=""),
#     html.Div(style=tabs_styles, id='tabs-example-content-1')
# ])


@app.callback(
    Output('tabs-example-content-1', 'children'),
    Input('tabs', 'active_tab')
)
# @app.callback(
#     Output('tabs-example-content-1', 'children'),
#     Input('tabs-example-1', 'value')
# )
def update_output(fig_name):
    return name_to_figure(fig_name)


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
                        color='rgb(227, 227, 230)',
                        size=17,
                        family="Roboto"
                    ),
                    fill_color='#2b2b2b',
                    line_color="#2b2b2b",
                    align="center",
                    height=27
                ),
                cells=dict(
                    values=[df2[xy].tolist() for xy in df2.columns[0:]],
                    # line_color=[np.array(colors)[arr1], np.array(colors)[arr2]],
                    line_color="#1f1e1e",
                    fill_color="rgb(3, 3, 3)",
                    font_color="rgb(201, 202, 204)",
                    align='center',
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
                    color="rgb(201, 202, 204)",
                    family="Balto"
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
            # html.H3('Tab content 1'),
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
                                  title=dict(
                                      text="Date",
                                      font={
                                          "size": 24
                                      }
                                  ),
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
                      hovermode='x unified',
                      hoverlabel=dict(namelength=-1, font_size=18, ),
                      paper_bgcolor="rgb(17,17,17)",
                      plot_bgcolor="rgb(17,17,17)",
                      font={
                          "color": "rgb(247, 246, 246)",
                          "family": "Balto"
                      },
                      title=go.layout.Title(
                          x=0.48,
                          text='Cholera Outbreak - London 1854',
                          font={
                              "color": "rgb(247, 246, 246)",
                              "family": "Balto"
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
        return html.Div([
            # html.H3('Tab content 2'),
            dcc.Graph(
                figure=fig
            )
        ])


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)

# Apply layout

# Connect plotly graphs with Dash Components

