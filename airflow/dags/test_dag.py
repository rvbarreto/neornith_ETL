from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
with DAG(
    dag_id='test_dag',
    start_date=datetime(2021, 1, 1),
    schedule_interval='@daily',
    catchup=False,
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo "Hello World"',
    )

    task2 = BashOperator(
        task_id='task2',
        bash_command='echo "Hello World from task 2"',
    )
    task3 = BashOperator(
        task_id='task3',
        bash_command='echo "Hello World from task 3"',
    )

    task1 >> [task2, task3]