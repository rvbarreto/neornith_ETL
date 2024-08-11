from neornith_utils import json_content, reg_url
import boto3
import json
from datetime import datetime

def save_to_s3(data, bucket_name, file_name):
    '''Save data to S3 bucket'''
    s3 = boto3.client('s3')
    s3.put_object(Body=data, Bucket=bucket_name, Key=file_name)

def get_and_save_city_reg(city_code, reg_type, page):
    '''Get and save records to S3 bucket as a .json file'''
    today = datetime.today().strftime('%Y%m%d')
    j = json_content(reg_url(city_code, reg_type, page))
    save_to_s3(json.dumps(j), 'neornith-etl', f'data/wikiaves/raw/{today}_{city_code}_{reg_type}_{page}.json')
    return j

def lambda_handler(event, context):
    response = get_and_save_city_reg(event['city_code'], event['type'], event['page'])
    return response