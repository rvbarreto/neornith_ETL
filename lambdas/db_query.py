import boto3
import json
import psycopg2


s3_client = boto3.client('s3')

def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except:
        return False
        
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
    
    sql_query = event['sql_query']
    #sql_query = "SELECT * FROM Locals_BR WHERE local_id = 1100015"

    cursor.execute(sql_query)

    if cursor.description is None:
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
