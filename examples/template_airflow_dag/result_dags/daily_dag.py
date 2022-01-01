from datetime import timedelta
from airflow import DAG
from airflow.operators.sql import BranchSQLOperator
from airflow.utils.dates import days_ago


dag = DAG(
    dag_id="daily_dag",
    schedule_interval="0 0 * * *",
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=60),
    tags=["example", "example2"],
    params={"example_key": "example_value"},
)


sql_schema_1_table_1_task = BranchSQLOperator(
    task_id="sql_schema_1.table_1",
    dag=dag,
    sql="queries/sql_schema_1/table_1.sql",
    database="sql_schema_1",
)


if __name__ == "__main__":
    dag.cli()
