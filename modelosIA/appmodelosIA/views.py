# appmodelosIA/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Modelo

def index_modelos(request):
    return redirect('modelo')

def modelos_view(request):
    qs = Modelo.objects.all().order_by('nombre')

    # --- Lee filtros del querystring ---
    f_tipo = request.GET.get('tipo_tarea') or ""
    f_familia = request.GET.get('familia') or ""
    f_modalidad = request.GET.get('modalidad') or ""
    f_escalado = request.GET.get('requiere_escalado') or ""  # "si" / "no" / ""
    f_alpha = request.GET.get('usa_alpha') or ""             # "si" / "no" / ""
    f_kernel = request.GET.get('usa_kernel') or ""           # "si" / "no" / ""
    f_anio_desde = request.GET.get('anio_desde') or ""
    f_anio_hasta = request.GET.get('anio_hasta') or ""

    # --- Aplica filtros si vienen ---
    if f_tipo:
        qs = qs.filter(tipo_tarea=f_tipo)
    if f_familia:
        qs = qs.filter(familia=f_familia)
    if f_modalidad:
        qs = qs.filter(modalidad=f_modalidad)

    def _bool_filter(val, field):
        if val == "si":
            return {field: True}
        if val == "no":
            return {field: False}
        return {}

    qs = qs.filter(**_bool_filter(f_escalado, "requiere_escalado"))
    qs = qs.filter(**_bool_filter(f_alpha, "usa_alpha"))
    qs = qs.filter(**_bool_filter(f_kernel, "usa_kernel"))

    try:
        if f_anio_desde:
            qs = qs.filter(anio_inventado__gte=int(f_anio_desde))
    except ValueError:
        pass
    try:
        if f_anio_hasta:
            qs = qs.filter(anio_inventado__lte=int(f_anio_hasta))
    except ValueError:
        pass

    # ===== Choices seguros =====
    # Si el campo tiene choices definidos en models.py se usan;
    # si no, se generan a partir de los valores distintos en BD.
    def safe_choices(field_name):
        field = Modelo._meta.get_field(field_name)
        if field.choices:
            return field.choices
        vals = (Modelo.objects
                .values_list(field_name, flat=True)
                .distinct()
                .order_by(field_name))
        return [(v, v) for v in vals if v not in (None, "")]

    tipo_choices = safe_choices("tipo_tarea")
    familia_choices = safe_choices("familia")
    modalidad_choices = safe_choices("modalidad")

    context = {
        'lista_modelos': qs,
        'TipoTarea': tipo_choices,
        'Familia': familia_choices,
        'Modalidad': modalidad_choices,
        'f': {
            'tipo_tarea': f_tipo,
            'familia': f_familia,
            'modalidad': f_modalidad,
            'requiere_escalado': f_escalado,
            'usa_alpha': f_alpha,
            'usa_kernel': f_kernel,
            'anio_desde': f_anio_desde,
            'anio_hasta': f_anio_hasta,
        }
    }
    return render(request, 'index.html', context)

def show_modelo(request, modelo_id: int):
    modelo_obj = get_object_or_404(
        Modelo.objects.prefetch_related('parametros'), pk=modelo_id
    )
    return render(request, 'modelo_detail.html', {'modelo': modelo_obj})
