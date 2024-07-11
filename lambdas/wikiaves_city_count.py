from neornith_utils import city_reg_count

def lambda_handler(event, context):
    response = city_reg_count(event['city_code'], event['type'])
    return response