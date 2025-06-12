import pytest
import pandas as pd
from datetime import datetime
from batch import prepare_data

# Helper function to create datetime objects
def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def test_prepare_data():
    # Input data
    data = [
        (None, None, dt(1, 1), dt(1, 10)),  
        (1, 1, dt(1, 2), dt(1, 10)),        
        (1, None, dt(1, 2, 0), dt(1, 2, 59)), 
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),   
    ]
    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df_input = pd.DataFrame(data, columns=columns)

    
    expected_data = [
        (1, 1, dt(1, 2), dt(1, 10), 8.0),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1), 60.016666666666666),
    ]
    expected_columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'duration']
    df_expected = pd.DataFrame(expected_data, columns=expected_columns)
    print('expected ',df_expected)
    
    df_actual = prepare_data(df_input)

    
    pd.testing.assert_frame_equal(
        df_actual.reset_index(drop=True), 
        df_expected.reset_index(drop=True)
    )

if __name__ == "__main__":
    test_prepare_data()