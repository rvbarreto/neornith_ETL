import boto3
import csv
import json

def lambda_handler(event, context):
    # Get the S3 bucket and file name from the event
    s3_bucket = 'neornith-etl'
    s3_key = event['csv_file']
    
    # Create an S3 client
    s3_client = boto3.client('s3')
    
    # Download the CSV file from S3
    response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
    csv_data = response['Body'].read().decode('utf-8')
    
    # Parse the CSV data
    reader = csv.DictReader(csv_data.splitlines())
    rows = [row for row in reader]
    
    # Serialize the data as JSON
    json_data = json.dumps(rows)
    
    # Invoke the other Lambda function with the JSON data
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(
        FunctionName='db-query-from-S3',
        InvocationType='RequestResponse',
        Payload=f'{{"bulk": {json_data}, "sql_file_name": "{event["sql_file_name"]}"}}'
    )
    
    return {
        'statusCode': 200,
        'body': 'CSV data processed successfully',
        'response': json.loads(response["Payload"].read())
    }