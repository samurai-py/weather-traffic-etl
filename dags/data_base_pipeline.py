from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta
import os

REDSHIFT_CONN_ID = os.environ.get('REDSHIFT_CONN_ID')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 17),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'create_table',
    default_args=default_args,
    description='DAG to create tables in Redshift',
    schedule_interval='@daily',
    catchup=False,
)

create_records_task = PostgresOperator(
    task_id='create_records_table',
    postgres_conn_id=REDSHIFT_CONN_ID,
    sql="""CREATE TABLE IF NOT EXISTS records (
        id BIGINT PRIMARY KEY IDENTITY(1, 1),
        uuid VARCHAR(100),
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    );""",
    dag=dag,
)

create_location_task = PostgresOperator(
    task_id='create_location_table',
    postgres_conn_id=REDSHIFT_CONN_ID,
    sql="""CREATE TABLE IF NOT EXISTS location (
        id INT PRIMARY KEY,
        name VARCHAR(100),
        region VARCHAR(100),
        country VARCHAR(100),
        lat FLOAT,
        lon FLOAT,
        tz_id VARCHAR(100)
    );""",
    dag=dag,
)

create_weather_task = PostgresOperator(
    task_id='create_weather_table',
    postgres_conn_id=REDSHIFT_CONN_ID,
    sql="""CREATE TABLE IF NOT EXISTS weather (
        id INT PRIMARY KEY IDENTITY(1, 1),
        record_id BIGINT REFERENCES records(id),
        location_id INT REFERENCES location(id),
        condition VARCHAR(100),
        temp_c FLOAT,
        temp_f FLOAT,
        is_day FLOAT,
        wind_mph FLOAT,
        pressure_mb FLOAT,
        precip_mm FLOAT,
        humidity FLOAT,
        cloud FLOAT,
        feelslike_c FLOAT,
        feelslike_f FLOAT,
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    );""",
    dag=dag,
)

create_directions_task = PostgresOperator(
    task_id='create_directions_table',
    postgres_conn_id=REDSHIFT_CONN_ID,
    sql="""CREATE TABLE IF NOT EXISTS directions (
        id INT PRIMARY KEY IDENTITY(1, 1),
        record_id BIGINT REFERENCES records(id),
        origin_id INT REFERENCES location(id),
        destination_id INT REFERENCES location(id),
        distance VARCHAR(100),
        trip_long VARCHAR(100),
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    );""",
    dag=dag,
)

create_records_task >> create_weather_task
create_weather_task >> create_directions_task
