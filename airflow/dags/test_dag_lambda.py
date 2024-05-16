
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import boto3
import json

def trigger_lambda_function():
    # Create a Boto3 client for Lambda
    lambda_client = boto3.client('lambda', region_name='us-east-1')

    # Specify the name of your Lambda function
    function_name = 'wikiaves-city-count'

    # Specify any input payload for your Lambda function
    payload = {
        'city_code': '1100015',
        'type': 'f'
    }

    # Invoke the Lambda function
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

    # Print the response from the Lambda function
    print(response)

# Define the DAG
dag = DAG(
    'trigger_lambda_wiki_count',
    description='DAG to trigger a Lambda function',
    schedule_interval=None,
    start_date=datetime(2022, 1, 1),
    catchup=False
)

# Define the task that triggers the Lambda function
trigger_lambda_task = PythonOperator(
    task_id='trigger_lambda_task',
    python_callable=trigger_lambda_function,
    dag=dag
)

# Set the task dependencies
trigger_lambda_task
