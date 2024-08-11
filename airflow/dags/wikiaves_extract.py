from airflow.decorators import task, dag
from functions.lambdas import trigger_lambda_function, execute_sql_file
from datetime import datetime
import time
from random import randint


@task()
def get_city_list():
    payload = {'sql_file_name': 'select_wa_outdated_cities.sql'}
    response = execute_sql_file(payload)
    return response
    #[[1100015, 0],[1100023, 2],[1100031, 20],...,[5300108, 1],[5300109, 40],[5300110, 3]]

def n_pages(total_reg, page_size=20):
    '''return the number of pages given the total of registers'''
    return((total_reg//page_size)+int(total_reg % page_size > 0))

@task()
def update_raw(city_ids):
    function_name = 'wikiaves-get-registers'
    for city_id, delta in city_ids:
        total = 0
        #for page in range(int(n_pages(delta) * 1.5)):
        page = 1 #
        while True: #
            payload = {
            'city_code': city_id,
            'type': 'f',
            'page': page
            }
            response = trigger_lambda_function(function_name, payload)
            response_len = len(response['registros']['itens'])
            if response_len == 0:
                break 
            page += 1 #
            total += response_len
            time.sleep(randint(1, 5)/10)
            print(f"Page {page} of city {city_id} processed.")
        print(f"{total}/{delta} registers inserted in raw layer for city {city_id}.")


@dag('wikiaves_extract', start_date=datetime(2021, 12, 1), schedule="0 0 * * 1", catchup=False)
def wikiaves_extract():
    city_ids = get_city_list()
    update_raw(city_ids)

dag = wikiaves_extract()