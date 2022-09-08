import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
from plotly.colors import n_colors


colors = n_colors('rgb(252, 211, 182)', 'rgb(250, 105, 2)', 40, colortype='rgb')

df = pd.read_table('data/naplesCholeraAgeSexData.tsv', header=6)
# print(df)

fig = make_subplots(
    rows=3, cols=2,
    shared_xaxes=True,
    vertical_spacing=0.05,
    specs=[
            [{"colspan": 2}, {"type": "bar"}],
            [{"type": "table"}, None],
            [{},{}]]
)

fig.add_trace(
    go.Table(
        header=dict(
            values=["Age", "Male", "Female"],
            font=dict(color='white', size=13),
            fill_color='blue',
            align="center"
        ),
        cells=dict(
            values=[df[xy].tolist() for xy in df.columns[0:]],
            line_color=[np.array(colors)[df['male'].to_numpy(int)], np.array(colors)[df['female'].to_numpy(int)]],
            fill_color=[np.array(colors)[df['male'].to_numpy(int)], np.array(colors)[df['female'].to_numpy(int)]],
            align='center')
        ),
    row=2, col=1
)

fig.add_trace(
    trace=go.Bar(
        x=df['age'],
        y=df['male'],
        name='Male',
        marker=dict(color='#0824c4')
    ),
    row=1, col=1
)

fig.add_trace(
    trace=go.Bar(
        x=df['age'],
        y=df['female'],
        name='Female',
        marker=dict(color='#c4084a')
    ),
    row=1, col=1
)

fig.update_layout(
    height=975,
    showlegend=True,
    title_text='NaplesCholera'
)

pyo.plot(fig, filename='NaplesCholera.html')
