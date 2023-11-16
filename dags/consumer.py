from airflow import DAG
from airflow import Dataset
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd
import statistics as sts

dag_dataset = Dataset('/opt/airflow/data/Churn_New.csv')

dag = DAG('dag_consumer', description='Python Code Three', schedule=[dag_dataset], start_date=datetime(2023, 3, 5), catchup=False)

def read_file():
    df = pd.read_csv('/opt/airflow/data/Churn_New.csv', sep=';')
    df.to_csv('/opt/airflow/data/Churn_New2.csv', sep=';')
    
task1 = PythonOperator(task_id='tsk1', python_callable=read_file, dag=dag, provide_context=True)

task1