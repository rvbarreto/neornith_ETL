
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from functions.lambdas import trigger_lambda_function

function_name = 'db-query-from-s3'
payload = {
    'sql_file_name': 'city_count.sql',
    'city': '1100015'
}

# Define the DAG
dag = DAG(
    'db_city_count',
    description='DAG to return the current count of registers in a city in neornith database',
    schedule_interval=None,
    start_date=datetime(2022, 1, 1),
    catchup=False
)

# Define the task that triggers the Lambda function
trigger_lambda = PythonOperator(
    task_id='trigger_lambda_db_city_count',
    python_callable=trigger_lambda_function,
    op_kwargs={'function_name': function_name, 'payload': payload},
    dag=dag
)

# Set the task dependencies
trigger_lambda
