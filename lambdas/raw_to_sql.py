import json
import boto3

# Create a lambda client
lambda_client = boto3.client('lambda')

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
    
def bulk_insert(table, fields, bulk_data):
    response = lambda_client.invoke(
        FunctionName='db-bulk-insert-to-sql',
        InvocationType='RequestResponse',
        Payload=f'{{"bulk": {bulk_data}, "table": "{table}", "fields": "{fields}"}}'
    )
    return response

def lambda_handler(event, context):
    # Get the S3 bucket and key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Read the JSON file from S3
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket, Key=key)
    json_data = response['Body'].read().decode('utf-8')
    
    # Parse the JSON data
    data = json.loads(json_data)
    
    # Normalize the data
    normalized_data = normalize_data(data['registros']['itens'])
    json_data = json.dumps(normalized_data)
    
    # Add species
    species_data = json.dumps([(r[1], r[3]) for r in normalized_data])
    fields = "binomial_name, pt_br"
    response_species = bulk_insert("Bird_Species", fields, species_data)
    
    # Add photos
    fields = "reg_id, binomial_name, sp_id, sp_wiki, autor, autor_perfil, reg_date, questionado, local_id, coms, likes, vis"
    response_photos = bulk_insert("Wikiaves_Photos", fields, json_data)
    
    return {
        'statusCode': 200,
        'body': 'Data normalized and saved to RDS PostgreSQL',
        'response': {
            'new_species': json.loads(response_species["Payload"].read()),
            'new_photos': json.loads(response_photos["Payload"].read())
        }
    }