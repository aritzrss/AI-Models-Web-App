from django.db import models

# Create your models here.
from django.db import models

# Primero, definimos el modelo principal
class Modelo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()    
    imagen_dashboard = models.ImageField(upload_to='dashboard_images/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

# Ahora, creamos un modelo para los parámetros
# Cada parámetro estará relacionado con un 'Modelo'
class Parametro(models.Model):
    modelo = models.ForeignKey(Modelo, related_name='parametros', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    valor = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre}: {self.valor} (para {self.modelo.nombre})"
