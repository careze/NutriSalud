from django import forms
from .models import Producto, Menu

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['foto', 'nombreProducto', 'categoria', 'precio', 'marca', 'stock', 'descripcion']
        widgets = {
            'categoria': forms.CheckboxSelectMultiple,  
        }

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['foto', 'nombreMenu', 'categoria', 'precio', 'stock', 'descripcion']
        widgets = {
            'categoria': forms.CheckboxSelectMultiple,  
        }