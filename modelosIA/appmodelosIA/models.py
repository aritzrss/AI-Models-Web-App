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


# --- Modelo principal: info + filtros ---
class Modelo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    imagen_dashboard = models.ImageField(upload_to="dashboard_images/")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Filtros principales
    tipo_tarea = models.CharField(
        max_length=25, choices=TIPO_TAREA_CHOICES, help_text="Tipo de tarea principal"
    )
    familia = models.CharField(
        max_length=20, choices=FAMILIA_CHOICES, help_text="Familia/algoritmo"
    )
    modalidad = models.CharField(
        max_length=15, choices=MODALIDAD_CHOICES, default="tabular",
        help_text="Modalidad de datos típica"
    )
    requiere_escalado = models.BooleanField(
        default=False, help_text="¿Requiere escalado de características?"
    )
    usa_alpha = models.BooleanField(
        default=False, help_text="¿Usa parámetro de regularización α (Ridge/Lasso, etc.)?"
    )
    usa_kernel = models.BooleanField(
        default=False, help_text="¿Usa kernel (SVM, etc.)?"
    )
    anio_inventado = models.PositiveSmallIntegerField(
        null=True, blank=True, db_index=True,
        help_text="Año aproximado de invención/publicación"
    )

    def __str__(self):
        return self.nombre


# --- Parámetros informativos (pares clave-valor) por modelo ---
# Relación 1─N: un Modelo tiene muchos parámetros.
class Parametro(models.Model):
    modelo = models.ForeignKey(
        Modelo, on_delete=models.CASCADE, related_name="parametros"
    )
    nombre = models.CharField(max_length=100)
    valor = models.CharField(max_length=200)

    class Meta:
        unique_together = ("modelo", "nombre")
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre}: {self.valor} (para {self.modelo.nombre})"
