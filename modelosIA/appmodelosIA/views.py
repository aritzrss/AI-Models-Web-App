from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Modelo

# Create your views here.

#primera vista sencilla de prueba
def index_modelos(request):
    return HttpResponse("App de modelos IA")

def modelos_view(request):
    "Vista para la página de detalles de modelos."
    modelos = get_list_or_404(Modelo.objects.order_by('nombre'))
    context = {'lista_modelos': modelos}
    return render(request, 'index.html', context)

def show_modelo(request, modelo_id):
    """
    Esta vista recibe un 'id' desde la URL, busca el modelo
    correspondiente y lo pasa a la plantilla de detalle.
    """
    modelo_obj = get_object_or_404(Modelo, pk=modelo_id)
    context = {
        'modelo': modelo_obj
    }
    return render(request, 'modelo_detail.html', context)
