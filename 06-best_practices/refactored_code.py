import pandas as pd

def read_data(categorical, year, month):
    
    input_file = f'https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    df = pd.read_parquet(input_file)
    
    for column in categorical:
        df[column] = df[column].astype('category')

    return df


def main(year, month):
    
    categorical = ['PULocationID', 'DOLocationID']
    
    df = read_data(categorical, year, month)
    
    output_file = f'taxi_type=yellow_year={year:04d}_month={month:02d}.parquet'
    df.to_parquet(output_file, engine='pyarrow', index=False)
    print(f"Data saved to {output_file}")


if __name__ == "__main__":
    
    year = 2023
    month = 3
    main(year, month)