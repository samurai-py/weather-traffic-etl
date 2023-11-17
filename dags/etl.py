from airflow.decorators import dag
from airflow.operators.bash_operator import BashOperator
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
    "run_scripts_daily",
    start_date=datetime(2021, 12, 1),
    max_active_runs=1,
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
)
def run_scripts_daily():
    # Use BashOperator to run Bash commands

    opr_run_extract = BashOperator(
        task_id="run_extract",
        bash_command="python ../src/etl/extract.py",
    )

    opr_run_pre_validate = BashOperator(
        task_id="run_pre_validate",
        bash_command="python ../src/validators/pre_validate.py",
    )

    opr_run_transform = BashOperator(
        task_id="run_transform",
        bash_command="python ../src/etl/transform.py",
    )

    opr_run_pos_validate = BashOperator(
        task_id="run_pos_validate",
        bash_command="python ../src/validators/pos_validate.py",
    )

    opr_run_load = BashOperator(
        task_id="run_load",
        bash_command="python ../src/etl/load.py",
    )

    # Set task dependencies
    opr_run_extract #>> opr_run_pre_validate >> opr_run_transform >> opr_run_pos_validate >> opr_run_load

run_scripts_daily_dag = run_scripts_daily()
