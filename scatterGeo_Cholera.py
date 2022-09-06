import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
import random

import warnings
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
        lat=lat1,
        lon=lon1,
        mode='markers',
        marker=dict(
            size=4
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
            color='rgb(255,0,0)'
        ),
        name= "Pump Location",
        hovertemplate='<b>Pump No: </b>%{text}<extra></extra>',
        text=df2["Pump No."].values.tolist(),
        hoverinfo="text+lat+lon",
    )
)

fig.update_layout(
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
        x=0.8,
        font=dict(
            size=22,
            color="rgb(201, 202, 204)",
            family="Balto"
        )
    ),
    autosize=True,
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
                lat=df.loc[:k+1,'Lat'],
                lon=df.loc[:k+1, 'Lon']
            )],
    traces=[0],
    name=f'frame{k}'
)for k in range(len(df))]

fig.update(frames=frames)

sliders = [dict(steps=[dict(method='animate',
                            args=[[f'frame{k}'],
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

fig.update_layout(updatemenus=[dict(type='buttons', showactive=True,
                                    y=0,
                                    x=1.05,
                                    xanchor='right',
                                    yanchor='top',
                                    pad=dict(t=0, r=10),
                                    buttons=[dict(label='Play',
                                                  method='animate',
                                                  args=[None,
                                                        dict(frame=dict(duration=100,
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

pyo.plot(fig, filename='scatterboxmap.html')
