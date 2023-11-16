from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from datetime import datetime, timedelta

default_args = {
    'depends_on_past': False,
    'start_date': datetime(2023, 3,5),
    'email': ['teste@teste.com'],
    'email_on_fail': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=8)
}

dag = DAG('default_args', 
          description='DAG com padrões', 
          default_args=default_args,
          schedule_interval='@daily', 
          start_date=datetime(2023, 3, 5), 
          catchup=False,
          default_view='graph',
          tags=['´preprocessing', 'tag', 'pipeline'])

task1 = BashOperator(task_id='tsk1', bash_command="sleep 5", dag=dag, retries=3)
task2 = BashOperator(task_id='tsk2', bash_command="sleep 5", dag=dag)
task3 = BashOperator(task_id='tsk3', bash_command="sleep 5", dag=dag)


task1 >> task2 >> task3
