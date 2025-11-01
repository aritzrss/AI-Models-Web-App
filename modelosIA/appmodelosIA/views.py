from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

#primera vista sencilla de prueba
def index_modelos(request):
    return HttpResponse("Listado de modelos IA")