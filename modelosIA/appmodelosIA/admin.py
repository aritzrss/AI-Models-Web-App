from django.contrib import admin
from .models import Modelo, Parametro


# Filtro sencillo por rangos de año (opcional y breve)
class AnioInventadoFilter(admin.SimpleListFilter):
    title = "Año de invención"
    parameter_name = "anio"

    def lookups(self, request, model_admin):
        return [
            ("<=1970", "≤ 1970"),
            ("1971-1999", "1971–1999"),
            (">=2000", "≥ 2000"),
            ("sin", "Sin dato"),
        ]

    def queryset(self, request, qs):
        v = self.value()
        if v == "<=1970":    return qs.filter(anio_inventado__lte=1970)
        if v == "1971-1999": return qs.filter(anio_inventado__gte=1971, anio_inventado__lte=1999)
        if v == ">=2000":    return qs.filter(anio_inventado__gte=2000)
        if v == "sin":       return qs.filter(anio_inventado__isnull=True)
        return qs


# Inline para editar parámetros dentro del modelo
class ParametroInline(admin.TabularInline):
    model = Parametro
    extra = 1


class ModeloIAAdmin(admin.ModelAdmin):
    list_display  = ("nombre", "tipo_tarea", "familia", "modalidad", "anio_inventado", "fecha_creacion")
    list_filter   = ("tipo_tarea", "familia", "modalidad", "requiere_escalado", "usa_alpha", "usa_kernel", AnioInventadoFilter)
    search_fields = ("nombre", "descripcion")
    ordering      = ("nombre",)
    inlines       = [ParametroInline]


admin.site.register(Modelo, ModeloIAAdmin)

