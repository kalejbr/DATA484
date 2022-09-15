import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
from plotly.colors import n_colors

# colors = n_colors('rgb(252, 211, 182)', 'rgb(250, 105, 2)', 8552262, colortype='rgb')

df = pd.read_csv('data/UKcensus1851.csv',header=2)
df2 = pd.read_csv('data/UKcensus1851.csv',header=2)
new_row = pd.DataFrame({'age':'Total', 'male':df['male'].sum(), 'female':df['female'].sum()}, index=[len(df)])
df = pd.concat([new_row, df.loc[:]]).sort_index()
df2 = pd.concat([new_row, df2.loc[:]]).sort_index()
df['all'] = df['male']+df['female']
df2['all'] = df2['male']+df2['female']

arr1 = df['male'].to_numpy()
arr2 = df['female'].to_numpy()
df2.loc[:, "male"] = df2["male"].map('{:,d}'.format)
df2.loc[:, "female"] = df2["female"].map('{:,d}'.format)
df2.loc[:, "all"] = df2["all"].map('{:,d}'.format)

datum = ['male', 'female']

fig = make_subplots(
    rows=3, cols=2,
    shared_xaxes=True,
    vertical_spacing=0.05,
    specs=[[{"type": "table"},{"type": "pie"}],
            [{"type": "pie"},{"type": "pie"}],
           [{"colspan":2},{"type": "bar"}]]
)

fig.add_trace(
    go.Table(
        header=dict(
            values=["Age", "Male", "Female", "All"],
            font=dict(
                color='rgb(227, 227, 230)',
                size=17,
                family="Arial"
            ),
            fill_color='#2b2b2b',
            line_color="#2b2b2b",
            align="center",
            height=26
        ),
        cells=dict(
            values=[df2[xy].tolist() for xy in df2.columns[0:]],
            # line_color=[np.array(colors)[arr1], np.array(colors)[arr2]],
            font=dict(
                family='Arial'
            ),
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
    row=1,col=2
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
    trace = go.Bar(
        x = df['age'],
        y = df[datum[0]],
        name = datum[0],
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
    row=3,col=1
)
fig.add_trace(
    trace = go.Bar(
        x = df['age'],
        y = df[datum[1]],
        name = datum[1],
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
    row=3,col=1
)

fig.update_layout(
    # annotations=[dict(),],
    height=1100,
    width=1400,
    showlegend=False,
    title=dict(
        text='UK Census 1851',
        x=0.5,
        font=dict(
            size=26,
            color="rgb(201, 202, 204)",
            family="Balto"
        )
    ),
    paper_bgcolor= "rgb(3, 3, 3)",
    plot_bgcolor= "rgb(3, 3, 3)",
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
    ),
    margin={
            "t": 100,
            "l": 200,
            "b": 150,
            "r": 20,
            "pad": 30
           }
)

# fig.show()
pyo.plot(fig, filename='UK1851census.html')
