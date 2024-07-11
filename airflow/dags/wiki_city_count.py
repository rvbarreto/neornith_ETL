from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from functions.lambdas import trigger_lambda_function

function_name = 'wikiaves-city-count'
payload = {
    'city_code': '1100015',
    'type': 'f'
}

# Define the DAG
dag = DAG(
    'wiki_city_count',
    description='DAG to return the current count of registers in a city currently in Wikiaves',
    schedule_interval=None,
    start_date=datetime(2022, 1, 1),
    catchup=False
)

# Define the task that triggers the Lambda function
trigger_lambda = PythonOperator(
    task_id='trigger_lambda_wiki_city_count',
    python_callable=trigger_lambda_function,
    op_kwargs={'function_name': function_name, 'payload': payload},
    dag=dag
)

# Set the task dependencies
trigger_lambda
#test
