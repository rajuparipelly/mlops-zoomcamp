#!/usr/bin/env python
# coding: utf-8

import sys
import pickle
import pandas as pd
import os


with open("model.bin", "rb") as f_in:
    dv, lr = pickle.load(f_in)


def prepare_data(df, categorical):

    df["duration"] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df["duration"] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype("int").astype("str")

    return df


def read_data(filename, categorical):

    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")

    if S3_ENDPOINT_URL is not None:
        options = {"client_kwargs": {"endpoint_url": S3_ENDPOINT_URL}}

        #df = pd.read_parquet(filename, storage_options=options)
        df = pd.read_parquet(filename)
    else:
        df = pd.read_parquet(filename)

    df = prepare_data(df, categorical)

    return df


def save_data(filename, df):

    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")

    if S3_ENDPOINT_URL is not None:
        options = {"client_kwargs": {"endpoint_url": S3_ENDPOINT_URL}}

        #df.to_parquet(filename, engine="pyarrow", index=False, storage_options=options)
        df.to_parquet(filename, engine="pyarrow", index=False)
    else:
        df.to_parquet(filename, engine="pyarrow", index=False)


def get_input_path(year, month):
    default_input_pattern = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet"
    #input_pattern = os.getenv("INPUT_FILE_PATTERN", default_input_pattern)
    #return input_pattern.format(year=year, month=month)
    return f"data/yellow_tripdata_{year:04d}-{month:02d}.parquet"


def get_output_path(year, month):
    #default_output_pattern = "s3://nyc-duration-912/taxi_type=fhv/year={year:04d}/month={month:02d}/predictions.parquet"
    #output_pattern = os.getenv("OUTPUT_FILE_PATTERN", default_output_pattern)
    #return output_pattern.format(year=year, month=month)
    return f"data/predictions.parquet"


def main(year, month):

    categorical = ["PULocationID", "DOLocationID"]

    input_file = get_input_path(year, month)
    output_file = get_output_path(year, month)

    df = read_data(input_file, categorical)
    df["ride_id"] = f"{year:04d}/{month:02d}_" + df.index.astype("str")

    dicts = df[categorical].to_dict(orient="records")
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    print("predicted sum duration:", y_pred.sum())

    df_result = pd.DataFrame()
    df_result["ride_id"] = df["ride_id"]
    df_result["predicted_duration"] = y_pred

    save_data(output_file, df_result)


if __name__ == "__main__":

    year = int(sys.argv[1])
    month = int(sys.argv[2])

    main(year, month)