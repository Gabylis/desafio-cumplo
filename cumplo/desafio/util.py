from datetime import datetime
from django.conf import settings
import requests,json

def get_computed_data(data,type_data,date_from,date_to):

    if type_data == 'uf':
        data_key  = 'UFs'
    else:
        data_key  = 'Dolares'

    data        = json.loads(data.text)
    data        = normalize_data(data[data_key],date_from,date_to)
    average     = sum(item["value"] for item in data) / len(data)
    highest     = max(data, key=lambda x:x['value'])
    lowest      = min(data, key=lambda x:x['value'])

    response    = {
            'avg'       : average,
            'highest'   : highest,
            'lowest'    : lowest,
            'data'      : data
        }

    return response

def format_float(value):
    return value.replace('.','').replace(',','.')

def normalize_data(data,date_from,date_to):
    result      = []
    for item in data:
        new_date = datetime.strptime(item["Fecha"], '%Y-%m-%d')
        if(date_from <= new_date <= date_to):
            result.append({
                'value' :   float(format_float(item["Valor"])),
                'date'  :   new_date
            })
    return result

def convert_to_chart_data(data):
    result      = []
    for item in data:
        result.append({
            'date' :    item["date"].strftime("%Y-%m-%d"),
            'close' :   item["value"]
        })
    return result

def make_api_call(date_from,date_to,type_data):
    request_url = settings.SBIF_BASE_URL % (
            type_data,
            date_from.year,
            date_from.month,
            date_to.year,
            date_to.month,
            settings.SBIF_AK,
            settings.SBIF_FORMAT
        )

    response = requests.get(request_url)
    return response
