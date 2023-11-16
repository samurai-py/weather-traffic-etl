# Domine Apache Airflow. https://www.eia.ai/
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator


dag =  DAG('db', description="database",
        schedule_interval=None,start_date=datetime(2023,3,5),
        catchup=False)

def print_result(ti):
    task_instance = ti.xcom_pull(task_ids='query_data')
    print("Resultado da consulta:")
    for row in task_instance:
        print(row)

create_table = PostgresOperator(task_id='create_table',
                                postgres_conn_id='postgres',
                                sql='create table if not exists teste(id int);',
                                dag=dag)

insert_data = PostgresOperator(task_id='insert_data',
                                postgres_conn_id='postgres',
                                sql='insert into teste values(1);',
                                dag=dag)

query_data = PostgresOperator(task_id='query_data',
                                postgres_conn_id='postgres',
                                sql='select * from teste;',
                                dag=dag)

print_task_result = PythonOperator(
                              task_id='print_task_result',
                              python_callable=print_result,
                              provide_context=True,
                              dag=dag   
                                )
create_table >> insert_data >> query_data >> print_task_result