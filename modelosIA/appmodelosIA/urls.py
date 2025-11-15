from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_modelos, name='index'),
    path('modelos/', views.modelos_view, name='modelo'),
    path('modelos/<int:modelo_id>/', views.show_modelo, name='modelo_detail'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('modelos/reporte/', views.reporte_view, name='reporte'),
]