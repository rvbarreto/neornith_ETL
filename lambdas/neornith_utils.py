import requests
import time
import json

def reg_url(c, tm, p=1):
    # {
    # o: {'dp':'mais recente'},
    # tm: {'f':'foto', 's':'som'}
    # }
    params = "tm={tm}&t=c&c={c}&p={p}&o=dp".format(tm=tm, c=c, p=p)
    return "https://www.wikiaves.com.br/getRegistrosJSON.php?" + params

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

def json_content(url):
    '''return json response of an url'''
    status = 0
    while not status == 200:
        try:
            r = requests.get(url)
            status = r.status_code
            if not validateJSON(r.text):
                print('[1]', end='')
                status = 0
                time.sleep(20)

        except requests.exceptions.RequestException as e:
            print('[0]', end='')
            status = 0
            time.sleep(20)
    return json.loads(r.text)

def city_reg_count(city_code, reg_type):
    '''return the current count of registers in a city'''
    j = json_content(reg_url(city_code, reg_type))
    return int(j['registros']['total'])