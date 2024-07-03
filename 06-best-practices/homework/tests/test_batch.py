import pytest
import batch 
import pandas as pd

from datetime import datetime

from deepdiff import DeepDiff


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def test_prepare_data():

    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)

    categorical = ['PULocationID', 'DOLocationID']
    df_prepared = batch.prepare_data(df, categorical)


    # Check for size of result rows for our test data
    assert df_prepared.shape[0] == 2, 'Rows number is incorrect'

    # Check if categorical columns are int
    assert all(df_prepared[categorical].map(lambda x: x.isdigit()))

    # Check if there is a duration column
    assert 'duration' in df_prepared.columns

    # Check if duration executed successfully and its between 1 and 60
    assert df_prepared['duration'].between(1, 60).all(), 'All duration should be between 1 and 60'

    # Check if duration is calculated correctly
    # assert df_prepared['duration'].equals(pd.Series([9.0, 8.0])), 'Is duration correct?'
    diff = DeepDiff(df_prepared['duration'], pd.Series([9.0, 8.0]))
    assert diff == {}, 'Is duration correct?'

    # Check if categorical columns are processed correctly
    # assert df_prepared[categorical].equals(pd.DataFrame({'PULocationID': ['-1', '1'], 'DOLocationID': ['-1', '1']})), 'Incorrected categorical!'
    diff = DeepDiff(df_prepared[categorical], pd.DataFrame({'PULocationID': ['-1', '1'], 'DOLocationID': ['-1', '1']}))
    assert diff == {}, 'Incorrected categorical!'

    