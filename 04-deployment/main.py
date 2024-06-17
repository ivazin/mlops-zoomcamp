import pickle
import pandas as pd
import os

YEAR = int(os.getenv('YEAR', 2023))
MONTH = int(os.getenv('MONTH', 3))

with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


# df = read_data('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_????-??.parquet')
# df = read_data('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet')
url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{YEAR:04d}-{MONTH:02d}.parquet'

print('getting url:', url)

df = read_data(url)

df['ride_id'] = f'{YEAR:04d}/{MONTH:02d}_' + df.index.astype('str')

dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)

print('Mean predicted:', y_pred.mean())

df_result = df[['ride_id']]
df_result.insert(1, 'predictions', y_pred)


df_result.to_parquet(
    f'output_tmp_{YEAR:04d}-{MONTH:02d}.parquet',
    engine='pyarrow',
    compression=None,
    index=False
)