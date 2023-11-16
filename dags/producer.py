from airflow import DAG
from airflow import Dataset
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd
import statistics as sts

dag = DAG('dag_producer', description='Python Code Two', schedule_interval=None, start_date=datetime(2023, 3, 5), catchup=False)

dag_dataset = Dataset('/opt/airflow/data/Churn_New.csv')

def read_file():
    df = pd.read_csv('/opt/airflow/data/Churn.csv', sep=';')
    df.to_csv('/opt/airflow/data/Churn_New.csv', sep=';')
    
task1 = PythonOperator(task_id='tsk1', python_callable=read_file, dag=dag, outlets=[dag_dataset])

task1