import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.offline as pyo


df = pd.read_table('data/choleraDeaths.tsv')
cols = ["Today's Attacks",'Total Attacks',"Today's Deaths",'Total Deaths']

data = []

for col in cols:
    trace = go.Scatter(
        x = df['Date'],
        y = df[col],
        mode = 'lines',
        name = col
    )
    data.append(trace)

# Define the layout
layout = go.Layout(
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
    xaxis=go.layout.XAxis(
        type="category",
        range=[
                8.143835616438356,
                32.631506849315066
            ],
        title=dict(
            text="Date",
            font={
                "size":16
            }
        ),
        nticks=18,
        tickson="labels",
        tickfont={
            "size": 14,
            "color":  "rgb(213, 213, 214)"
        },
        gridcolor= "rgb(55, 66, 82)",
        gridwidth=0,
        tickangle=45,
        rangeslider={
            "range": [0,41],
            "yaxis": {"rangemode":"match"},
            "visible": True,
            "autorange": True,
            "thickness": 0.07,
            "borderwidth":2
        },
        zerolinewidth=0,
        zerolinecolor="rgb(70, 114, 138)"
    ),
    yaxis= go.layout.YAxis(
        zerolinewidth=0,
        zerolinecolor="rgb(55, 66, 82)",
        type="linear",
        range=[
                -34.22222222222222,
                650.2222222222222
        ],
        title=dict(
            text="# of Individuals",
            font={
                "size": 16
            }
        ),
        tickson='boundaries',
        gridwidth=0,
        gridcolor= "rgb(34, 41, 51)",
        tickfont={
            "size": 16,
            "color": "rgb(213, 213, 214)"
        },
        autorange=True,
        tickangle=0
    ),
    margin={
        "t": 42,
        "pad": 13
    },
    autosize=True,
    hovermode='x unified',
    hoverlabel=dict(
        font={
            "family":"Balto",
            "color":"rgb(213, 213, 214)"
        },
        align= "right",
        namelength=-1,
        font_size=18,
    ),
    showlegend=False
)

fig = go.Figure(data=data,layout=layout)
fig.update_layout()

pyo.plot(fig, filename='Cholera_A&D.html')