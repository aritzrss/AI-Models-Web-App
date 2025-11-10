from django.contrib import admin

# Register your models here.
from .models import Modelo

class ModeloIAAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_creacion')
    search_fields = ['nombre', 'descripcion']
    
admin.site.register(Modelo, ModeloIAAdmin)