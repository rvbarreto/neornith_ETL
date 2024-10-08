import boto3
import json
import psycopg2
from psycopg2.sql import SQL, Literal


s3_client = boto3.client('s3')

def execute_query(cursor, sql_file_content, event):
    placeholders = {key: Literal(value) for key, value in event.items()}
    query = SQL(sql_file_content).format(**placeholders)
    cursor.execute(query)

def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except:
        return False
        
def lambda_handler(event, context):
    # Get the name of the SQL file from the event parameter
    sql_file_name = event['sql_file_name']

    # Retrieve the SQL file from the S3 bucket
    s3_bucket = 'neornith-etl'
    s3_key = f'sql-queries/{sql_file_name}'
    response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
    sql_file_content = response['Body'].read().decode('utf-8')
    
    # Get the PostgreSQL secrets
    s3_key = "secrets/rds_db_secret.json"
    response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
    db_secrets = json.loads(response['Body'].read().decode('utf-8'))

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=db_secrets['host'],
        port=db_secrets['port'],
        database=db_secrets['database'],
        user=db_secrets['username'],
        password=db_secrets['password']
    )
    conn.autocommit = True

    cursor = conn.cursor()
    #sql_file_content = "SELECT * FROM Locals_BR WHERE local_id = 1100015"

    ## Execute the SQL query
    if 'bulk' in event:
        for record in event['bulk']:
            execute_query(cursor, sql_file_content, record)
    else:
        execute_query(cursor, sql_file_content, event)

    if cursor.description is None:
        cursor.close()
        conn.close()
        return None
    
    results = cursor.fetchall()
    
    # Close the database connection
    cursor.close()
    conn.close()

    # Return the query results
    if is_jsonable(results):
        return results
    else:
        return json.dumps(results, default=str)
