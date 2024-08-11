import json
import boto3

import logging
logger = logging.getLogger()
logger.setLevel("ERROR")
logger.info("raw to sql started")


def extract_data(item):
    d = dict()
    d['reg_id'] = item['id']
    d['reg_type'] = item['tipo']
    d['sp_id'] = item['sp']['id']
    d['sp_cientifico'] = item['sp']['nome']
    d['sp_popular'] = item['sp']['nvt']
    d['sp_wiki'] = item['sp']['idwiki']
    d['reg_autor'] = item['autor']
    d['autor_perfil'] = item['perfil']
    d['reg_data'] = item['data']
    d['reg_questionado'] = item['is_questionada']
    d['reg_local'] = item['local']
    d['local_id'] = item['idMunicipio']
    d['reg_coms'] = item['coms']
    d['reg_likes'] = item['likes']
    d['reg_vis'] = item['vis']
    return(d)

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
    
    # Normalize the data using your custom function
    normalized_data = normalize_data(data['registros']['itens'])
    json_data = json.dumps(normalized_data)
    

    # Create a lambda client
    lambda_client = boto3.client('lambda')

    logger.info(f'Updating city {normalized_data[0]['local_id']}...')
    # Call db query lambda function and pass the normalized data to it
    response = lambda_client.invoke(
        FunctionName='db-query-from-S3',
        InvocationType='RequestResponse',
        Payload=f'{{"bulk": {json_data}, "sql_file_name": "insert_bird_photos.sql"}}'
    )
    logger.info('Done!')
    logger.info('Updating table count')
    # Update city count in the database
    lambda_client.invoke(
        FunctionName='db-query-from-S3',
        InvocationType='Event',
        Payload=f'{{"sql_file_name": "update_db_city_count.sql", "local_id": {normalized_data[0]['local_id']}}}'
    )
    logger.info('Done!')
    
    return {
        'statusCode': 200,
        'body': 'Data normalized and saved to RDS PostgreSQL',
        'response': json.loads(response["Payload"].read()),
    }