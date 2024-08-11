from airflow.decorators import task, dag
from functions.lambdas import trigger_lambda_function, execute_sql_file
from datetime import datetime
import time
from random import randint

def wiki_city_count(city_id):
    function_name = 'wikiaves-city-count'
    payload = {
        'city_code': city_id,
        'type': 'f'
    }

    while True:
        try:
            response = int(trigger_lambda_function(function_name, payload))
            break
        except:
            time.sleep(randint(5, 20)/10)
            print(f"Error getting wikiaves city {city_id} count. Retrying...")
            continue
    
    return response

@task()
def get_city_list():
    payload = {
        'sql_file_name': 'select_cities_by_update_date.sql'
    }
    response = execute_sql_file(payload)
    return response
    #[[1100015],[1100023],[1100031],...,[5300108],[5300109],[5300110]]

@task()
def update_counts(city_ids):
    for city_id in city_ids:
        wa_count = wiki_city_count(city_id[0])
        print(f"{city_id[0]}: {wa_count} new registers.")
        payload = {
            'sql_file_name': 'update_wa_city_count.sql',
            'local_id': city_id[0],
            'db_wikiaves': wa_count
        }
        execute_sql_file(payload)
        print(f"Saved")
        time.sleep(randint(1, 5)/10)

@dag('wikiaves_update_counts',
     schedule_interval='0 0 * * 0',
     start_date=datetime(2022, 1, 1),
     catchup=False)
def wikiaves_update_counts():
    city_ids = get_city_list()
    update_counts(city_ids)

dag = wikiaves_update_counts()