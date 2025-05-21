from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import sys

# Allow importing scripts from ../scripts
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from fetch_weather import fetch_weather
from transform_data import transform_weather
from load_to_db import load_to_postgres

default_args = {
    'start_date': datetime(2025, 5, 21),
    'retries': 1,
}

with DAG(
    dag_id='weather_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=["weather", "ETL"],
) as dag:

    fetch = PythonOperator(
        task_id='fetch_weather',
        python_callable=fetch_weather
    )

    transform = PythonOperator(
        task_id='transform_weather',
        python_callable=transform_weather
    )

    load = PythonOperator(
        task_id='load_to_postgres',
        python_callable=load_to_postgres
    )

    fetch >> transform >> load
