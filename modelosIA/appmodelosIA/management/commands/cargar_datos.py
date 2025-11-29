"""

Para ejecutarlo, al nivel de la carpeta modelosIA escribimos en terminal:

        python manage.py cargar_datos
        
Con esto se borrarán TODOS los modelos y toda la información de la Base de Datos
y se cargarán únicamente los modelos que aquí hemos implementado.

"""

from django.core.management.base import BaseCommand
from appmodelosIA.models import Modelo, Dataset, MLDataset, MLAlgorithm, MLParametro
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = 'Carga datos iniciales para la aplicación (Seed Data)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('⚠️  Borrando datos antiguos...'))
        
        # Limpiar base de datos
        MLParametro.objects.all().delete()
        MLAlgorithm.objects.all().delete()
        MLDataset.objects.all().delete()
        Modelo.objects.all().delete()
        Dataset.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('✓ Base de datos limpia.'))

        self.stdout.write('Creando datos para el Laboratorio ML...')

        # Datasets (sklearn)
        iris = MLDataset.objects.create(nombre="Iris Plants", clave="iris", tipo_tarea="clasificacion")
        diab = MLDataset.objects.create(nombre="Diabetes", clave="diabetes", tipo_tarea="regresion")
        wine = MLDataset.objects.create(nombre="Wine Quality", clave="wine", tipo_tarea="clasificacion")
        digit = MLDataset.objects.create(nombre="Handwritten Digits", clave="digits", tipo_tarea="clasificacion")

        # Algoritmos y Parámetros
        # KNN
        knn = MLAlgorithm.objects.create(nombre="K-Nearest Neighbors", clave="knn_cls", tipo_tarea="clasificacion")
        MLParametro.objects.create(algoritmo=knn, nombre="n_neighbors", valor="5", tipo_dato="int")

        # Random Forest
        rf = MLAlgorithm.objects.create(nombre="Random Forest", clave="rf_reg", tipo_tarea="regresion")
        MLParametro.objects.create(algoritmo=rf, nombre="n_estimators", valor="100", tipo_dato="int")
        MLParametro.objects.create(algoritmo=rf, nombre="max_depth", valor="10", tipo_dato="int")

        # Regresión Lineal
        linear = MLAlgorithm.objects.create(nombre="Regresión Lineal", clave="linear", tipo_tarea="regresion")

        # K-Means
        kmeans = MLAlgorithm.objects.create(nombre="K-Means", clave="kmeans", tipo_tarea="clustering")
        MLParametro.objects.create(algoritmo=kmeans, nombre="n_clusters", valor="3", tipo_dato="int")

        # PCA
        pca = MLAlgorithm.objects.create(nombre="PCA", clave="pca", tipo_tarea="reduccion")
        MLParametro.objects.create(algoritmo=pca, nombre="n_components", valor="2", tipo_dato="int")

        self.stdout.write(self.style.SUCCESS(f'✓ {MLAlgorithm.objects.count()} Algoritmos creados.'))

        # ==========================================
        # 3. CREAR DATOS PARA EL DASHBOARD (Fichas)
        # ==========================================
        self.stdout.write('Creando datos para el Dashboard...')

        # Datasets informativos (Categorías)
        cat_iris = Dataset.objects.create(nombre="Iris Dataset", descripcion="Datos de flores iris.")
        cat_casas = Dataset.objects.create(nombre="California Housing", descripcion="Precios de casas.")

        # Modelos de Ejemplo
        # Nota: Creamos una imagen dummy pequeña para que no falle el campo ImageField
        dummy_image = ContentFile(b'fake_image_bytes', name='sample.jpg')

        Modelo.objects.create(
            nombre="Clasificador Iris V1",
            descripcion="Modelo base utilizando KNN para clasificar flores.",
            tipo_tarea="clasificacion",
            familia="distancia",
            modalidad="tabular",
            anio_inventado=2023,
            dataset=cat_iris,
            rating_promedio=4.5,
            cantidad_votos=10,
            imagen_dashboard=dummy_image
        )

        Modelo.objects.create(
            nombre="Predicción Precios Casas",
            descripcion="Regresión lineal simple para estimar precios en California.",
            tipo_tarea="regresion",
            familia="lineal",
            modalidad="tabular",
            anio_inventado=1990,
            dataset=cat_casas,
            rating_promedio=3.2,
            cantidad_votos=5,
            imagen_dashboard=dummy_image
        )

        self.stdout.write(self.style.SUCCESS(f'✓ {Modelo.objects.count()} Fichas de modelos creadas.'))
        self.stdout.write(self.style.SUCCESS('🎉 CARGA DE DATOS COMPLETADA CORRECTAMENTE'))