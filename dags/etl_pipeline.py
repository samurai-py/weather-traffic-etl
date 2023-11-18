from airflow.decorators import dag, task
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from src.etl import extract, transform, load
from src.validators import pre_validate, pos_validate

default_args = {
    "owner": "admin",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

@dag(
    "run_scripts_daily",
    start_date=datetime(2021, 12, 1),
    max_active_runs=1,
    schedule_interval="@hourly",
    default_args=default_args,
    catchup=False,
)
def run_scripts_daily():
    # Use BashOperator to run Bash commands

    opr_run_extract = PythonOperator(
        task_id="run_extract",
        python_callable=extract.run_extract,
    )
    
    opr_weather_pre_validate = PythonOperator(
    task_id="weather_pre_validate",
    python_callable=pre_validate.run_pre_validate,
    op_args=[
        '/usr/local/airflow/dags/src/data/weather_raw_data.csv',
        '/usr/local/airflow/dags/src/validators/validation_assets/cols/weather_cols.json'
    ],
)

    opr_directions_pre_validate = PythonOperator(
    task_id="directions_pre_validate",
    python_callable=pre_validate.run_pre_validate,
    op_args=[
        '/usr/local/airflow/dags/src/data/directions_raw_data.csv',
        '/usr/local/airflow/dags/src/validators/validation_assets/cols/directions_cols.json'
    ],
)

    opr_run_transform = PythonOperator(
        task_id="run_transform",
        python_callable=transform.run_transform,
    )
    
    opr_weather_pos_validate = PythonOperator(
    task_id="weather_pos_validate",
    python_callable=pos_validate.run_pos_validate,
    op_args=[
        '/usr/local/airflow/dags/src/data/weather_cleaned_data.csv',
        '/usr/local/airflow/dags/src/validators/validation_assets/cols/weather_cols.json',
        '/usr/local/airflow/dags/src/validators/validation_assets/cities.json'
    ],
)

    opr_directions_pos_validate = PythonOperator(
    task_id="directions_pos_validate",
    python_callable=pos_validate.run_pos_validate,
    op_args=[
        '/usr/local/airflow/dags/src/data/directions_cleaned_data.csv',
        '/usr/local/airflow/dags/src/validators/validation_assets/cols/directions_cols.json',
        '/usr/local/airflow/dags/src/validators/validation_assets/cities.json',
        ['origin_name_normalized', 'destination_name_normalized']
    ],
)

    opr_run_load_records = PythonOperator(
        task_id="run_load_records",
        python_callable=load.connect_and_insert,
        op_args=['records'],  # Argumentos adicionais para a função
    )

    opr_run_load_weather = PythonOperator(
        task_id="run_load_weather",
        python_callable=load.connect_and_insert,
        op_args=['weather'],  # Argumentos adicionais para a função
    )

    opr_run_load_directions = PythonOperator(
        task_id="run_load_directions",
        python_callable=load.connect_and_insert,
        op_args=['directions'],  # Argumentos adicionais para a função
    )

    # Set task dependencies
    opr_run_extract >> [opr_weather_pre_validate, opr_directions_pre_validate]
    [opr_weather_pre_validate, opr_directions_pre_validate] >> opr_run_transform 
    opr_run_transform >> [opr_weather_pos_validate, opr_directions_pos_validate ]
    [opr_weather_pos_validate, opr_directions_pos_validate ] >> opr_run_load_records
    opr_run_load_records >> [opr_run_load_weather, opr_run_load_directions]

run_scripts_daily_dag = run_scripts_daily()
