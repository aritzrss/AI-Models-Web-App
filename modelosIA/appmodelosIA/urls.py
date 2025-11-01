from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_modelos, name='index'),    #este path llama a la vista de los modelos
]