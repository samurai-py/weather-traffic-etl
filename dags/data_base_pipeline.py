from airflow.decorators import dag
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

@dag(
    "create_database_dag",
    start_date=datetime(2023, 11, 17),
    max_active_runs=1,
    schedule="@daily",
    default_args=default_args,
    template_searchpath="../src/etl/sql",
    catchup=False,
)
def create_database():
    opr_run_sql = SQLExecuteQueryOperator(
        task_id="run_sql",
        postgres_conn_id="redshift_wt",
        sql="create_tables.sql"
    )

create_database_dag = create_database()