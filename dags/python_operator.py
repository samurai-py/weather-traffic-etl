from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd
import statistics as sts

dag = DAG('python_operator', description='Python Code One', schedule_interval=None, start_date=datetime(2023, 3, 5), catchup=False)

def data_cleaner():
    
    df = pd.read_csv('/opt/airflow/data/Churn.csv', sep=';')
    df.columns = ['Id', 'Score', 'State', 'Gender', 'Age', 'Wealth','Balance', 'Products', 'HasCC', 'Status', 'Salary', 'Exit']
    median_salary = sts.median(df['Salary'])
    
    df['Salary'].fillna(median_salary, inplace=True)
    
    df['Gender'].fillna('Masculino', inplace=True)
    
    median_age = sts.median(df['Age'])
    
    df.loc[(df['Age'] < 0 ) | (df['Age'] > 120), 'Age'] = median_age
    
    df.drop_duplicates(subset='Id', keep='first', inplace=True)
    
    df.to_csv('/opt/airflow/data/Churn_Cleaned.csv', sep=';', index=False)
    
task1 = PythonOperator(task_id='tsk1', python_callable=data_cleaner, dag=dag)

task1