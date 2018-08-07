from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import datetime,requests,json
from . import util
from datetime import datetime

def home(request):
    type_data = 'uf'
    today = datetime.today()
    today_datetime = datetime.strptime(
        '%s-%s-%s' % (today.year,today.month,today.day),
        '%Y-%m-%d'
    )

    response = util.make_api_call(today_datetime,today_datetime,type_data)
    computed = util.get_computed_data(response,type_data,today_datetime,today_datetime)

    return render(request,'desafio/index.html',{
        'data'      : computed['data'],
        'highest'   : computed['highest'],
        'lowest'    : computed['lowest'],
        'avg'       : computed['avg'],
        'chart_data': json.dumps(util.convert_to_chart_data(computed['data']))
    })


def get_data(request):
    type_data   = request.GET.get("type_data")
    date_from   = datetime.strptime(request.GET.get("date_from"), '%Y-%m-%d')
    date_to     = datetime.strptime(request.GET.get("date_to"), '%Y-%m-%d')

    response = util.make_api_call(date_from,date_to,type_data)
    computed = util.get_computed_data(response,type_data,date_from,date_to)

    return render(request,'desafio/index.html',{
        'data'      : computed['data'],
        'highest'   : computed['highest'],
        'lowest'    : computed['lowest'],
        'avg'       : computed['avg'],
        'chart_data': json.dumps(util.convert_to_chart_data(computed['data']))
    })

def get_chart_data(request):
    type_data   = request.GET.get("type_data")
    date_from   = datetime.strptime(request.GET.get("date_from"), '%Y-%m-%d')
    date_to     = datetime.strptime(request.GET.get("date_to"), '%Y-%m-%d')

    response = util.make_api_call(date_from,date_to,type_data)
    computed = util.get_computed_data(response,type_data,date_from,date_to)
    return HttpResponse(json.dumps(util.convert_to_chart_data(computed['data'])),content_type="application/json")
