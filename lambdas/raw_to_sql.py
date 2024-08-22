import json
import boto3

import logging
logger = logging.getLogger()
logger.setLevel("ERROR")
logger.info("raw to sql started")

def extract_data(item):
    l = list()
    l.append(item['id'])
    l.append(item['sp']['nome'])
    l.append(item['sp']['id'])
    l.append(item['sp']['idwiki'])
    l.append(item['autor'])
    l.append(item['perfil'])
    l.append(item['data'])
    l.append(item['is_questionada'])
    l.append(item['idMunicipio'])
    l.append(item['coms'])
    l.append(item['likes'])
    l.append(item['vis'])
    return(tuple(l))

def normalize_data(data):
    normalized_data = [extract_data(record) for key, record in data.items()]
    return normalized_data

def lambda_handler(event, context):
    logger.info(event)
    
    # Get the S3 bucket and key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Read the JSON file from S3
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket, Key=key)
    json_data = response['Body'].read().decode('utf-8')
    
    # Parse the JSON data
    data = json.loads(json_data)
    
    logger.info("raw data loaded")
    
    # Normalize the data
    normalized_data = normalize_data(data['registros']['itens'])
    json_data = json.dumps(normalized_data)
    
    # Create a lambda client
    lambda_client = boto3.client('lambda')

    logger.info(f'Updating city {normalized_data[0]['local_id']}...')
    fields = "reg_id, binomial_name, sp_id, sp_wiki, autor, autor_perfil, reg_date, questionado, local_id, coms, likes, vis"
    # Call db query lambda function and pass the normalized data to it
    response = lambda_client.invoke(
        FunctionName='db-bulk-insert-to-sql',
        InvocationType='RequestResponse',
        Payload=f'{{"bulk": {json_data}, "table": "Wikiaves_Photos", "fields": "{fields}"}}'
    )
    logger.info('Done!')
    
    return {
        'statusCode': 200,
        'body': 'Data normalized and saved to RDS PostgreSQL',
        'response': json.loads(response["Payload"].read()),
    }