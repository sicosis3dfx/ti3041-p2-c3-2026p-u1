from django import forms
from .models import Contacto
 
class ContactoForm(forms.ModelForm):
    class Meta: 
        model = Contacto
        fields = ['nombre', 'telefono', 'correo', 'direccion']
        labels = {
            'nombre': 'Nombre completo',
            'telefono': 'Teléfono',
            'correo': 'Correo electrónico',
            'direccion': 'Dirección',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej. María González'}),
            'telefono': forms.TextInput(attrs={'placeholder': '+56 9 1234 5678'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'nombre@ejemplo.com'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Calle, número y comuna'}),
        }