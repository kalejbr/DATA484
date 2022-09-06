import pandas as pd
import random

df = pd.read_csv('data/choleraDeathLocations.csv')
lat1 = df.Lat
lon1 = df.Lon

random.Random(3).shuffle(lat1)
random.Random(3).shuffle(lon1)
random.Random(3).shuffle(df['Deaths'])

frames= [dict(data=[dict(
                lat=df.loc[:k+1, 'Lat'],
                lon=df.loc[:k+1, 'Lon']
            )],
            traces=[0],
            name=f'frame{k}'
)for k in range(len(df))]

print(frames)
