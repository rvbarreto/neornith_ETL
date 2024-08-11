import boto3
import json

def trigger_lambda_function(function_name, payload, region_name='us-east-1'):
    lambda_client = boto3.client('lambda', region_name=region_name)
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    json_payload = json.loads(response['Payload'].read().decode('utf-8'))
    return json_payload

def execute_sql_file(payload):
    function_name = 'db-query-from-S3'
    payload = payload
    try:
        response = trigger_lambda_function(function_name, payload)
    except:
        print("Error executing SQL file with payload: ", payload)
    return response