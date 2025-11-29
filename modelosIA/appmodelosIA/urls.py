from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_modelos, name='index'), 
    path('modelos/', views.modelos_view, name='modelo'),
    path('modelos/<int:modelo_id>/', views.show_modelo, name='modelo_detail'),
    path('modelos/reporte/', views.reporte_view, name='reporte'),
    path('votar/<int:modelo_id>/', views.votar_modelo, name='votar_modelo'),
    path('modelos/nuevo/', views.crear_modelo_view, name='crear_modelo'),
    path('modelos/borrar/<int:modelo_id>/', views.borrar_modelo_view, name='borrar_modelo'),
]