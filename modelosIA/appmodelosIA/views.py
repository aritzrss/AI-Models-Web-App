from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse # <--- AÑADIDO JsonResponse
from django.template.loader import render_to_string # <--- AÑADIDO para AJAX
from datetime import datetime
import base64
from io import BytesIO
from .models import Modelo, Dataset, MLDataset, MLAlgorithm, TIPO_TAREA_CHOICES, FAMILIA_CHOICES, MODALIDAD_CHOICES
import matplotlib
matplotlib.use('Agg') #necesario para navegadores web, así no se abre una ventana con el gráfico
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, confusion_matrix, ConfusionMatrixDisplay, silhouette_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier
from .forms import ModeloForm 
from .models import Modelo
def crear_modelo_view(request):
    if request.method == 'POST':
        # Cargamos los datos (request.POST) y la imagen (request.FILES)
        form = ModeloForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Se redirige al usuario al listado de modelos
            return redirect('modelo')
    else:
        # Si es GET, mostramos el formulario vacío
        form = ModeloForm()

    return render(request, 'crear_modelo.html', {'form': form})

def index_modelos(request):
    print("\n[LOG] Usuario en: Página de Inicio (Dashboard)")
    
    ultimos_modelos = Modelo.objects.all().exclude(anio_inventado__isnull=True).order_by('-anio_inventado')[:3]
    return render(request, 'index.html', {'ultimos_modelos': ultimos_modelos})

def votar_modelo(request, modelo_id):
    if request.method == 'POST':
        modelo = get_object_or_404(Modelo, pk=modelo_id)
        puntuacion_str = request.POST.get('puntuacion')
        try:
            puntuacion = int(puntuacion_str)
            if 1 <= puntuacion <= 5:
                print(f"\n[LOG] Acción: Voto recibido ({puntuacion} estrellas) para {modelo.nombre}")
                modelo.agregar_voto(puntuacion)
        except (ValueError, TypeError):
            print("\n[LOG] Error: Intento de voto inválido")
            pass 
    return redirect('modelo_detail', modelo_id=modelo_id)

def show_modelo(request, modelo_id: int):
    modelo_obj = get_object_or_404(Modelo.objects.prefetch_related('parametros'), pk=modelo_id)
    
    print(f"\n[LOG] Viendo detalles del modelo: {modelo_obj.nombre}")
    
    return render(request, 'modelo_detail.html', {'modelo': modelo_obj})

def borrar_modelo_view(request, modelo_id):
    modelo = get_object_or_404(Modelo, pk=modelo_id)
    
    if request.method == 'POST':
        # Si el usuario confirma (envía el formulario), borramos.
        modelo.delete()
        # Redirigimos al listado principal porque este modelo ya no existe
        return redirect('modelo')
        
    # Si es GET, mostramos la página de confirmación
    return render(request, 'confirmar_borrado.html', {'modelo': modelo})

def modelos_view(request):
    print("\n[LOG] Usuario en: Página de Buscador/Filtros")
    
    qs = Modelo.objects.all().order_by('nombre')

    # Filtros
    f_dataset = request.GET.get('dataset', '')
    f_orden = request.GET.get('orden', '')
    f_tipo = request.GET.get('tipo_tarea', '')
    f_familia = request.GET.get('familia', '')
    f_modalidad = request.GET.get('modalidad', '')
    f_escalado = request.GET.get('requiere_escalado', '')
    f_alpha = request.GET.get('usa_alpha', '')
    f_kernel = request.GET.get('usa_kernel', '')
    f_anio_desde = request.GET.get('anio_desde', '')
    f_anio_hasta = request.GET.get('anio_hasta', '')

    if f_dataset: qs = qs.filter(dataset__id=f_dataset)
    if f_tipo: qs = qs.filter(tipo_tarea=f_tipo)
    if f_familia: qs = qs.filter(familia=f_familia)
    if f_modalidad: qs = qs.filter(modalidad=f_modalidad)
    if f_escalado == "si": qs = qs.filter(requiere_escalado=True)
    elif f_escalado == "no": qs = qs.filter(requiere_escalado=False)
    if f_alpha == "si": qs = qs.filter(usa_alpha=True)
    elif f_alpha == "no": qs = qs.filter(usa_alpha=False)
    if f_kernel == "si": qs = qs.filter(usa_kernel=True)
    elif f_kernel == "no": qs = qs.filter(usa_kernel=False)
    if f_anio_desde and f_anio_desde.isdigit(): qs = qs.filter(anio_inventado__gte=int(f_anio_desde))
    if f_anio_hasta and f_anio_hasta.isdigit(): qs = qs.filter(anio_inventado__lte=int(f_anio_hasta))

    if f_orden == 'dataset': qs = qs.order_by('dataset__nombre')
    elif f_orden == 'mejor_valorado': qs = qs.order_by('-rating_promedio')
    elif f_orden == 'peor_valorado': qs = qs.order_by('rating_promedio')
    elif f_orden == 'mas_votado': qs = qs.order_by('-cantidad_votos')
    else: qs = qs.order_by('nombre')

    datasets_disponibles = Dataset.objects.all()

    context = {
        'lista_modelos': qs,
        'TipoTarea': TIPO_TAREA_CHOICES, 'Familia': FAMILIA_CHOICES, 'Modalidad': MODALIDAD_CHOICES,
        'Datasets': datasets_disponibles,
        'f': {
            'tipo_tarea': f_tipo, 'familia': f_familia, 'modalidad': f_modalidad,
            'requiere_escalado': f_escalado, 'usa_alpha': f_alpha, 'usa_kernel': f_kernel,
            'anio_desde': f_anio_desde, 'anio_hasta': f_anio_hasta,
            'dataset': f_dataset, 'orden': f_orden,
        }
    }
    return render(request, 'formulario.html', context)


CLASES_MAP = {
    # Datasets
    'iris': datasets.load_iris,
    'diabetes': datasets.load_diabetes,
    'wine': datasets.load_wine,
    'digits': datasets.load_digits,
    # Modelos
    'logistic': LogisticRegression,
    'dt_cls': DecisionTreeClassifier,
    'svm_cls': SVC,
    'knn_cls': KNeighborsClassifier,
    'linear': LinearRegression,
    'rf_reg': RandomForestRegressor,
    'svm_reg': SVR,
    'kmeans': KMeans,
    'pca': PCA,
}

def fig_to_base64(fig):
    """Convierte la gráfica en memoria a texto Base64 para el HTML"""
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    plt.close(fig)
    return f"data:image/png;base64,{image_base64}"

def ejecutar_analisis_dinamico_db(dataset_obj, algo_obj):
    
    print(f"\n[LOG] Ejecutando laboratorio: Cargando {algo_obj.nombre} para {dataset_obj.nombre}")
    
    # Cargar Datos
    load_function = CLASES_MAP.get(dataset_obj.clave)
    if not load_function: raise ValueError(f"Dataset no soportado: {dataset_obj.clave}")
    
    raw_data = load_function()
    X, y = raw_data.data, raw_data.target
    
    # Instanciar Modelo
    ModelClass = CLASES_MAP.get(algo_obj.clave)
    if not ModelClass: raise ValueError(f"Algoritmo no soportado: {algo_obj.clave}")
    
    params = algo_obj.get_params_dict()
    
    # Ajuste automático para KMeans
    if algo_obj.clave == 'kmeans' and 'n_clusters' not in params:
        params['n_clusters'] = len(set(y)) if y is not None else 3
        
    modelo = ModelClass(**params)
    
    resultado = {
        'dataset': dataset_obj.nombre,
        'algoritmo': algo_obj.nombre,
        'tipo': algo_obj.tipo_tarea,
        'metricas': {},
        'imagen': None
    }

    # Ejecución y Generación de Gráficas
    if algo_obj.tipo_tarea == 'reduccion':
        X_trans = modelo.fit_transform(X)
        resultado['metricas']['Varianza'] = f"{sum(modelo.explained_variance_ratio_)*100:.2f}%"
        
        # Plot PCA
        fig, ax = plt.subplots(figsize=(8, 6))
        scatter = ax.scatter(X_trans[:, 0], X_trans[:, 1], c=y, cmap='viridis', edgecolor='k')
        ax.set_title(f"PCA: {dataset_obj.nombre}")
        resultado['imagen'] = fig_to_base64(fig)

    elif algo_obj.tipo_tarea == 'clustering':
        y_pred = modelo.fit_predict(X)
        resultado['metricas']['Inercia'] = f"{modelo.inertia_:.2f}"
        if len(set(y_pred)) > 1:
            resultado['metricas']['Silhouette'] = f"{silhouette_score(X, y_pred):.3f}"
        
        # Plot Clusters
        pca_viz = PCA(n_components=2).fit_transform(X)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(pca_viz[:, 0], pca_viz[:, 1], c=y_pred, cmap='tab10')
        ax.set_title("Clusters (Vista PCA)")
        resultado['imagen'] = fig_to_base64(fig)

    else: # Supervisado
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)
        
        if algo_obj.tipo_tarea == 'regresion':
            resultado['metricas']['MSE'] = f"{mean_squared_error(y_test, y_pred):.2f}"
            resultado['metricas']['R²'] = f"{r2_score(y_test, y_pred):.3f}"
            
            # Plot Regresión
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.scatter(y_test, y_pred, color='blue', alpha=0.5)
            ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
            ax.set_title("Real vs Predicho")
            resultado['imagen'] = fig_to_base64(fig)

        elif algo_obj.tipo_tarea == 'clasificacion':
            resultado['metricas']['Accuracy'] = f"{accuracy_score(y_test, y_pred)*100:.1f}%"
            
            # Plot Matriz de Confusión
            fig, ax = plt.subplots(figsize=(6, 5))
            cm = confusion_matrix(y_test, y_pred)
            ConfusionMatrixDisplay(cm).plot(ax=ax, cmap='Blues')
            resultado['imagen'] = fig_to_base64(fig)

    return resultado

# -----------------------------------------------------------------------------
# VISTA MODIFICADA PARA SOPORTAR AJAX
# -----------------------------------------------------------------------------
def reporte_view(request):
    
    print("\n[LOG] Usuario en: Página de Reporte ML (Laboratorio)")
    
    datasets_db = MLDataset.objects.all()
    algos_db = MLAlgorithm.objects.all()
    
    sel_ds_id = request.GET.get('dataset_id')
    sel_algo_id = request.GET.get('algo_id')
    
    resultado = None
    error_msg = None
    
    # Esta lógica de ejecución es la misma
    if sel_ds_id and sel_algo_id:
        try:
            ds_obj = MLDataset.objects.get(pk=sel_ds_id)
            algo_obj = MLAlgorithm.objects.get(pk=sel_algo_id)
            resultado = ejecutar_analisis_dinamico_db(ds_obj, algo_obj)
        except Exception as e:
            error_msg = f"Error al ejecutar: {str(e)}"
            print(f"\n[LOG] Error en ejecución: {error_msg}")

    context = {
        'datasets_list': datasets_db,
        'models_list': algos_db,
        'sel_ds_id': int(sel_ds_id) if sel_ds_id else None,
        'sel_algo_id': int(sel_algo_id) if sel_algo_id else None,
        'resultado': resultado,
        'error': error_msg,
        'fecha_actual': datetime.now()
    }
    
    # Comprobamos si la petición es AJAX por la cabecera que añade 'fetch'
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        # Si es AJAX, renderizamos solo el fragmento de HTML y lo devolvemos en un JSON
        html = render_to_string('reporte_resultado.html', context, request=request)
        return JsonResponse({'html': html})
    
    # Si no es AJAX, renderizamos la página completa como se hacía originalmente
    return render(request, 'reporte.html', context)

def votar_modelo(request, modelo_id):
    # CASO 1: La petición es un POST (el usuario ha enviado el formulario)
    if request.method == 'POST':
        modelo = get_object_or_404(Modelo, pk=modelo_id)
        puntuacion_str = request.POST.get('puntuacion')

        try:
            puntuacion = int(puntuacion_str)
            if 1 <= puntuacion <= 5:
                modelo.agregar_voto(puntuacion)
        except (ValueError, TypeError):
            # Si el valor no es válido, simplemente no hacemos nada.
            pass


        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        # CASO 1A: Es un POST enviado vía AJAX
        if is_ajax:
            html = render_to_string(
                'valoracion.html', 
                {'modelo': modelo}, 
                request=request
            )
            return JsonResponse({'html': html}) # <-- RETURN para AJAX POST

        return redirect('modelo_detail', modelo_id=modelo_id) # <-- RETURN para NON-AJAX POST

    # CASO 2: La petición es un GET (o cualquier otro método)
    # Si alguien intenta acceder a la URL directamente, lo redirigimos.
    return redirect('modelo_detail', modelo_id=modelo_id) # <-- RETURN para GET
