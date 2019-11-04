from django.http import HttpResponse
from circuito_config.models import Datalog
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello World by Django")

def testaparametro(request, parametro_id):
    response = 'o Parametro da URL é: %s'
    return HttpResponse(response % parametro_id)

def retornoparametros(request):
    datalogger_list = Datalog.objects.all()
    context = {
        'datalogger_list': datalogger_list,
    }
    return render(request,'circuito_config/index.html', context)
