from datetime import timedelta
from airflow import DAG
from airflow.operators.sql import BranchSQLOperator
from airflow.utils.dates import days_ago


dag = DAG(
    dag_id='hourly_dag',
    schedule_interval='0 * * * *',
    start_date=days_ago(1),
    dagrun_timeout=timedelta(minutes=60),
    tags=['example', 'example2'],
    params={'example_key': 'example_value'},
)


sql_schema_1_table_2_task = BranchSQLOperator(
    task_id='sql_schema_1.table_2',
    dag=dag,
    sql='queries/sql_schema_1/table_2.sql',
    database='sql_schema_1'
)

sql_schema_2_table_3_task = BranchSQLOperator(
    task_id='sql_schema_2.table_3',
    dag=dag,
    sql='queries/sql_schema_2/table_3.sql',
    database='sql_schema_2'
)


sql_schema_1_table_2_task >> sql_schema_2_table_3_task

if __name__ == '__main__':
    dag.cli()



