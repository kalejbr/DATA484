import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.offline as pyo

# Currently plotly does not support smooth transition of animations other than scatter and bar charts
# This will continue to be a work in progress

df = pd.read_csv('data/UKcensus1851.csv',header=2)
fig = go.Figure()

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
        showlegend=False
    )
)

fig.show()
