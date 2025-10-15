from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

defaults_args = {"owner": "airflow"}

with DAG(
    dag_id="dbt_staging_dag",
    default_args=defaults_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    # ================================== dbt deps
    dbt_deps = BashOperator(
        task_id="dbt_deps",
        bash_command="cd /opt/airflow/dags/data_pipeline && dbt deps",
    )

    # ================================== run stg models
    dbt_stg = BashOperator(
        task_id="dbt_run_staging",
        bash_command="cd /opt/airflow/dags/data_pipeline && dbt run --select staging --target dev",
    )

    # ================================== run marts
    dbt_marts = BashOperator(
        task_id="dbt_run_marts",
        bash_command="cd /opt/airflow/dags/data_pipeline && dbt run --select marts --target dev",
    )

    dbt_deps >> dbt_stg >> dbt_marts
