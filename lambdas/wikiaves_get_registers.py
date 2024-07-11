from neornith_utils import json_content, reg_url
import boto3
import time
import json
from datetime import datetime

def n_pages(total_reg, page_size=20):
    '''return the number of pages given the total of registers'''
    return((total_reg//page_size)+int(total_reg % page_size > 0))

def save_to_s3(data, bucket_name, file_name):
    '''Save data to S3 bucket as a .json file'''
    s3 = boto3.client('s3')
    s3.put_object(Body=data, Bucket=bucket_name, Key=file_name)

def get_city_regs(city_code, reg_type, total):
    '''get all registers of a city'''
    n = n_pages(total)
    today = datetime.today().strftime('%Y%m%d')
    for p in range(n, 0, -1):
        j = json_content(reg_url(city_code, reg_type, p))
        save_to_s3(json.dumps(j), 'neornith-etl', f'data/wikiaves/raw/{today}_{city_code}_{reg_type}_{p}.json')
        time.sleep(0.1)
    return [city_code, reg_type, n]

def lambda_handler(event, context):
    response = get_city_regs(event['city_code'], event['type'], event['total'])
    return response