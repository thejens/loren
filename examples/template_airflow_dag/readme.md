# Template Airflow DAG

This is the original purpose of this library, rendering DAG files for airflow

This naive example illustrates a SQL workflow where tasks contain a query,
belong do different DAGs and outputs to tables based on where the config
files are stored.

Note how {% raw %} is used in jinja2 to keep some brackets for Airflow's
templating.

`python -m parender render --configuration-path examples/template_airflow_dag/config/ --template-path examples/template_airflow_dag/dag_template.py.j2 --output-path examples/template_airflow_dag/result_dags/`
