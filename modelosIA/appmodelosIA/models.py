from django.db import models

TIPO_TAREA_CHOICES = [
    ("clasificacion", "Clasificación"),
    ("regresion", "Regresión"),
    ("clustering", "Agrupamiento (Clustering)"),
    ("reduccion_dimensional", "Reducción dimensional"),
    ("generativo", "Generativo"),
]

FAMILIA_CHOICES = [
    ("lineal", "Lineal"),
    ("distancia", "Basado en distancia"),
    ("kernel", "Kernel"),
    ("arbol", "Árbol"),
    ("ensemble", "Conjunto (Ensemble)"),
    ("red_neuronal", "Red neuronal"),
    ("transformer", "Transformer"),
    ("proyeccion", "Proyección (PCA)"),
]

MODALIDAD_CHOICES = [
    ("tabular", "Tabular"),
    ("texto", "Texto"),
    ("vision", "Visión"),
]

# Tabla auxiliar para los Datasets del Dashboard (Filtros)
class Dataset(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Modelo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    imagen_dashboard = models.ImageField(upload_to="dashboard_images/")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Filtros principales
    tipo_tarea = models.CharField(max_length=25, choices=TIPO_TAREA_CHOICES)
    familia = models.CharField(max_length=20, choices=FAMILIA_CHOICES)
    modalidad = models.CharField(max_length=15, choices=MODALIDAD_CHOICES, default="tabular")
    requiere_escalado = models.BooleanField(default=False)
    usa_alpha = models.BooleanField(default=False)
    usa_kernel = models.BooleanField(default=False)
    anio_inventado = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True)

    # Relaciones y Valoraciones
    dataset = models.ForeignKey(Dataset, on_delete=models.SET_NULL, null=True, blank=True, related_name="modelos")
    rating_promedio = models.FloatField(default=0.0)
    cantidad_votos = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    def agregar_voto(self, puntuacion):
        total_puntos = self.rating_promedio * self.cantidad_votos
        self.cantidad_votos += 1
        self.rating_promedio = (total_puntos + puntuacion) / self.cantidad_votos
        self.save()

class Parametro(models.Model):
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, related_name="parametros")
    nombre = models.CharField(max_length=100)
    valor = models.CharField(max_length=200)

    class Meta:
        unique_together = ("modelo", "nombre")
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre}: {self.valor}"


# Modelos para el reporte
class MLDataset(models.Model):
    """Datasets disponibles para ejecutar en tiempo real (ej: Iris, Diabetes)"""
    nombre = models.CharField(max_length=50)   # Nombre visual (ej: Iris Plants)
    clave = models.CharField(max_length=50, unique=True) # Clave interna (ej: iris)
    tipo_tarea = models.CharField(max_length=20, choices=[
        ('clasificacion', 'Clasificación'),
        ('regresion', 'Regresión'),
    ])
    
    def __str__(self):
        return self.nombre

class MLAlgorithm(models.Model):
    """Algoritmos disponibles para seleccionar (ej: Random Forest)"""
    nombre = models.CharField(max_length=50)
    clave = models.CharField(max_length=50, unique=True) # Clave interna (ej: rf_reg)
    tipo_tarea = models.CharField(max_length=20, choices=[
        ('clasificacion', 'Clasificación'),
        ('regresion', 'Regresión'),
        ('clustering', 'Clustering'),
        ('reduccion', 'Reducción Dimensional'),
    ])

    def __str__(self):
        return self.nombre

    def get_params_dict(self):
        """Convierte los parámetros de la tabla hija a un diccionario Python"""
        params = {}
        for p in self.ml_parametros.all():
            val = p.valor
            
            if p.tipo_dato == 'int':
                val = int(val)
            elif p.tipo_dato == 'float':
                val = float(val)
            elif p.tipo_dato == 'bool':
                val = (val.lower() == 'true')
            params[p.nombre] = val
        return params

class MLParametro(models.Model):
    """Parámetros configurables para cada algoritmo (ej: n_estimators=100)"""
    algoritmo = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE, related_name="ml_parametros")
    nombre = models.CharField(max_length=50) # Ej: n_neighbors
    valor = models.CharField(max_length=50)  # Ej: 3 (guardado como texto)
    
    tipo_dato = models.CharField(max_length=10, choices=[
        ('str', 'Texto'),
        ('int', 'Entero'),
        ('float', 'Decimal'),
        ('bool', 'Booleano'),
    ], default='int')

    def __str__(self):
        return f"{self.nombre}={self.valor}"