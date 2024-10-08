import boto3
import json
import psycopg2
from psycopg2.extras import execute_values
        
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Get the PostgreSQL secrets
    s3_bucket = 'neornith-etl'
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

    table = event['table']
    bulk = event['bulk']
    fields = event['fields']
    template = event['template'] if 'template' in event else None

    insert_query = "SET datestyle = dmy; INSERT INTO " + table + " (" + fields + ") VALUES %s ON CONFLICT DO NOTHING RETURNING 1;"
    response = execute_values(cursor,
                              insert_query,
                              bulk,
                              template=template,
                              page_size=300,
                              fetch=True)

    # Close the database connection
    cursor.close()
    conn.close()
    
    return sum([r[0] for r in response])