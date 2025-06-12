import pandas as pd
import os
from datetime import datetime

import batch

#S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
#S3_ENDPOINT_URL = "output/yellow_tripdata_2023-01.parquet"

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


def test_integration():

    #options = {"client_kwargs": {"endpoint_url": S3_ENDPOINT_URL}}

    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
    ]

    columns = [
        "PULocationID",
        "DOLocationID",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
    ]
    df = pd.DataFrame(data, columns=columns)

    input_file = batch.get_input_path(2023, 1)
    output_file = batch.get_output_path(2023, 1)

    df.to_parquet(
        input_file,
        engine="pyarrow",
        compression=None,
        index=False,
        #storage_options=options,
    )

    os.system("python batch.py 2023 1")

    #df_actual = pd.read_parquet(output_file, storage_options=options)
    df_actual = pd.read_parquet(output_file)
    sum_predictions = df_actual["predicted_duration"].sum()
    print(f"sum of predictions: {sum_predictions}")

    assert (sum_predictions - 36.28) < 0.1

if __name__ == "__main__":
    test_integration()