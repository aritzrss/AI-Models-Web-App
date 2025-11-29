from django import forms
from .models import Modelo

class ModeloForm(forms.ModelForm):
    class Meta:
        model = Modelo
        # Campos que rellenará el usuario
        fields = [
            'nombre', 
            'descripcion', 
            'imagen_dashboard', 
            'tipo_tarea', 
            'familia', 
            'modalidad', 
            'requiere_escalado', 
            'usa_alpha', 
            'usa_kernel', 
            'anio_inventado',
            'dataset' # El usuario elige el dataset de la lista (iris, diabetes...)
        ]
        # Opcional: Para darle estilos CSS a los inputs
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Random Forest V2'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'anio_inventado': forms.NumberInput(attrs={'class': 'form-control'}),
        }