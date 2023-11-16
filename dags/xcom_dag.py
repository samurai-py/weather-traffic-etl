from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

dag = DAG('xcom_dag', description='DAG Xcom', schedule_interval=None, start_date=datetime(2023, 3, 5), catchup=False)

def task_write(**kwargs):
    kwargs['ti'].xcom_push(key='xcom_value1', value=8888)
    
def task_read(**kwargs):
    value = kwargs['ti'].xcom_pull(key='xcom_value1')
    print(f'Valor recuperado: {value}')
    

task1 = PythonOperator(task_id='tsk1', python_callable=task_write, dag=dag)
task2 = PythonOperator(task_id='tsk2', python_callable=task_read, dag=dag)


task1 >> task2
