import boto3
import json
import psycopg2
from psycopg2.sql import SQL, Literal

s3_client = boto3.client('s3')

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

    # Execute the SQL query
    placeholders = {key: Literal(value) for key, value in event.items()}
    query = SQL(sql_file_content).format(**placeholders)
    cursor.execute(query)

    if cursor.description is None:
        return None
    
    results = cursor.fetchall()
    
    # Close the database connection
    cursor.close()
    conn.close()
    
    # Return the query results
    return results