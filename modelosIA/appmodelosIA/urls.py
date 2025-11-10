from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_modelos, name='index'),
    path('modelo/', views.modelos_view, name='modelo'),
    path('modelo/<int:modelo_id>/', views.show_modelo, name='modelo_detail'),
]