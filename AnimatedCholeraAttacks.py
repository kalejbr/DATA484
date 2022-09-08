import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.offline as pyo


df = pd.read_table('data/choleraDeaths.tsv')
cols = ["Today's Attacks",'Total Attacks',"Today's Deaths",'Total Deaths']

df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].dt.date

data = []

for col in cols:
    trace = go.Scatter(
        x = df.Date[:1],
        y = df[col][:1],
        mode = 'lines',
        name = col,
    )
    data.append(trace)

layout = go.Layout(
    showlegend=False,
    hovermode='x unified',
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
              hoverlabel=dict(namelength=-1,font_size=18,),
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

frames = [dict(data= [dict(type='scatter',
                            x= df.Date[:k+1],
                            y= df[cols[0]][:k+1]),
                        dict(type='scatter',
                            x=df.Date[:k+1],
                            y=df[cols[1]][:k+1]),
                        dict(type='scatter',
                            x= df.Date[:k+1],
                            y= df[cols[2]][:k+1]),
                        dict(type='scatter',
                            x= df.Date[:k+1],
                            y= df[cols[3]][:k+1])],
               )for k in range(1, len(df[cols[0]]-1))]

fig = go.Figure(data=data, frames=frames, layout=layout)
fig.show()
