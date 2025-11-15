from django.shortcuts import render, get_object_or_404, redirect
from .models import Modelo, TIPO_TAREA_CHOICES, FAMILIA_CHOICES, MODALIDAD_CHOICES
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error, r2_score, silhouette_score
import pandas as pd
import base64
from io import BytesIO
from datetime import datetime


def index_modelos(request):
    return render(request, 'index.html')

def modelos_view(request):
    
    """
        El usuario realizará distintos filtrados para ver unos modelos u otros.
        Esta función explica paso a paso como se gestionan los filtrados.
        Para ello hemos realizado un formulario básico donde recogíamos las características y las cogíamos de la BD.
    """
    # 1. Empezamos con todos los modelos, ordenados por nombre
    qs = Modelo.objects.all().order_by('nombre')

    # 2. Leemos todos los posibles filtros que vienen en la URL (?param=valor&...)
    f_tipo = request.GET.get('tipo_tarea', '')
    f_familia = request.GET.get('familia', '')
    f_modalidad = request.GET.get('modalidad', '')
    f_escalado = request.GET.get('requiere_escalado', '')  # "si", "no", o ""
    f_alpha = request.GET.get('usa_alpha', '')             # "si", "no", o ""
    f_kernel = request.GET.get('usa_kernel', '')           # "si", "no", o ""
    f_anio_desde = request.GET.get('anio_desde', '')
    f_anio_hasta = request.GET.get('anio_hasta', '')

    # 3. Aplicamos los filtros uno por uno si el usuario los ha rellenado

    # Filtros de texto (selects)
    if f_tipo:
        qs = qs.filter(tipo_tarea=f_tipo)
    if f_familia:
        qs = qs.filter(familia=f_familia)
    if f_modalidad:
        qs = qs.filter(modalidad=f_modalidad)

    match f_escalado:
        case "si":
            qs = qs.filter(requiere_escalado=True)
        case "no":
            qs = qs.filter(requiere_escalado=False)
    
    match f_alpha:
        case "si":
            qs = qs.filter(usa_alpha=True)
        case "no":
            qs = qs.filter(usa_alpha=False)

    match f_kernel:
        case "si":
            qs = qs.filter(usa_kernel=True)
        case "no":
            qs = qs.filter(usa_kernel=False)

    # Filtros de año, asegurándonos de que son números antes de filtrar
    if f_anio_desde and f_anio_desde.isdigit():
        qs = qs.filter(anio_inventado__gte=int(f_anio_desde))
    
    if f_anio_hasta and f_anio_hasta.isdigit():
        qs = qs.filter(anio_inventado__lte=int(f_anio_hasta))

    # Tras todos los filtros, los añadimos al contexto que volcamos en el HTML
    context = {
        'lista_modelos': qs,
        'TipoTarea': TIPO_TAREA_CHOICES,
        'Familia': FAMILIA_CHOICES,
        'Modalidad': MODALIDAD_CHOICES,
        # Valores de los filtros
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
    return render(request, 'formulario.html', context)

def show_modelo(request, modelo_id: int):
    modelo_obj = get_object_or_404(
        Modelo.objects.prefetch_related('parametros'), pk=modelo_id
    )
    return render(request, 'modelo_detail.html', {'modelo': modelo_obj})

# Funciones auxiliares para realizar PCA y K-Means
def fig_to_base64(fig):
    """Convierte una figura de matplotlib a base64 para incrustar en HTML"""
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    plt.close(fig)
    return f"data:image/png;base64,{image_base64}"


def ejemplo_linear_regression():
    diabetes = datasets.load_diabetes()
    X, y = diabetes.data, diabetes.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo_lr = LinearRegression().fit(X_train, y_train)
    y_pred = modelo_lr.predict(X_test)
    coeficientes = pd.DataFrame({
        'Característica': diabetes.feature_names,
        'Coeficiente': modelo_lr.coef_
    }).sort_values('Coeficiente', key=abs, ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(y_test, y_pred, alpha=0.6, edgecolors='k', s=80)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=3, label='Predicción perfecta')
    ax.set_xlabel('Valores Reales', fontsize=13)
    ax.set_ylabel('Predicciones', fontsize=13)
    ax.set_title('Linear Regression: Predicciones vs Valores Reales', fontsize=15)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return {
        'n_muestras': X.shape[0],
        'n_caracteristicas': X.shape[1],
        'mse': mean_squared_error(y_test, y_pred),
        'r2': r2_score(y_test, y_pred),
        'coeficientes_df': coeficientes.to_dict('records'),
        'imagen': fig_to_base64(fig)
    }

def ejemplo_pca():
    iris = datasets.load_iris()
    X, y = iris.data, iris.target
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    componentes_df = pd.DataFrame(pca.components_.T, columns=['PC1', 'PC2'], index=iris.feature_names)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, especie in enumerate(iris.target_names):
        ax.scatter(X_pca[y == i, 0], X_pca[y == i, 1], label=especie, alpha=0.8, s=100, edgecolors='k')
    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% varianza)')
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% varianza)')
    ax.set_title('PCA del Dataset Iris', fontsize=15)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return {
        'n_muestras': X.shape[0],
        'n_caracteristicas_original': X.shape[1],
        'n_componentes': 2,
        'varianza_total': sum(pca.explained_variance_ratio_) * 100,
        'componentes_df': componentes_df.reset_index().rename(columns={'index':'Característica'}).to_dict('records'), 
        'imagen': fig_to_base64(fig)
    }

def ejemplo_kmeans():
    iris = datasets.load_iris()
    X = iris.data
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X)
    pca = PCA(n_components=2).fit_transform(X)
    centroides_pca = PCA(n_components=2).fit(X).transform(kmeans.cluster_centers_)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(pca[:, 0], pca[:, 1], c=clusters, cmap='viridis', alpha=0.7, s=100, edgecolors='k')
    ax.scatter(centroides_pca[:, 0], centroides_pca[:, 1], c='red', marker='X', s=250, label='Centroides')
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_title('K-Means Clustering del Dataset Iris', fontsize=15)
    ax.legend(*scatter.legend_elements(), title='Clusters')
    ax.grid(True, alpha=0.3)
    
    return {
        'n_muestras': X.shape[0],
        'n_clusters': 3,
        'silhouette': silhouette_score(X, clusters),
        'inercia': kmeans.inertia_,
        'imagen_clusters': fig_to_base64(fig)
    }

# Vista de los modelos implementados

def reporte_view(request):
    """
    Ejecuta los modelos de ML y muestra los resultados en una plantilla.
    """
    # 1. Ejecutar cada modelo para obtener los resultados
    resultados_lr = ejemplo_linear_regression()
    resultados_pca = ejemplo_pca()
    resultados_kmeans = ejemplo_kmeans()

    # 2. Crear el contexto para pasarlo a la plantilla
    context = {
        'fecha_actual': datetime.now(),
        'resultados_lr': resultados_lr,
        'resultados_pca': resultados_pca,
        'resultados_kmeans': resultados_kmeans,
    }

    # 3. Renderizar la plantilla con el contexto
    return render(request, 'reporte.html', context)
    
    