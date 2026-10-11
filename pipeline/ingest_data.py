#!/usr/bin/env python
# coding: utf-8
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import pandas as pd



def run():
    year = 2021
    month = 1

    pg_user = 'root'
    pg_password = 'root'
    pg_host = 'localhost'
    pg_port = '5432'

    chunksize = 100000
    target_Table = 'yellow_taxi_data'

    dtype = {
        "VendorID": "Int64",
        "passenger_count": "Int64",
        "trip_distance": "float64",
        "RatecodeID": "Int64",
        "store_and_fwd_flag": "string",
        "PULocationID": "Int64",
        "DOLocationID": "Int64",
        "payment_type": "Int64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64"
    }

    parse_dates = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime"
    ]

    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/ny_taxi')

    df_iter = pd.read_csv(
        'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz',

        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize,
    )
    first = True


    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')
            first = False
        df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

if __name__ == '__main__':
    run()
