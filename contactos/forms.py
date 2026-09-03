from django import forms
from django.core.validators import EmailValidator
from .models import Contacto


class ContactoForm(forms.ModelForm):
    """
    Formulario basado en el modelo Contacto.
    Permite la captura y validación de los datos personales requeridos en el Caso 3.
    """
    class Meta:
        model = Contacto
        # Campos requeridos por el Caso 3: nombre, teléfono, correo y dirección
        fields = ['nombre', 'telefono', 'correo', 'direccion']
        labels = {
            'nombre': 'Nombre completo',
            'telefono': 'Teléfono',
            'correo': 'Correo electrónico',
            'direccion': 'Dirección',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej. María González', 'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'placeholder': '+56 9 1234 5678', 'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'nombre@ejemplo.com', 'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Calle, número y comuna', 'class': 'form-control'}),
        }

    def clean_correo(self):
        """
        Requerimiento Caso 3: Validar formato de correo electrónico.
        Aplica validación de formato usando el paquete estándar django.core.validators.EmailValidator
        y estructuras de decisión (if).
        """
        correo = self.cleaned_data.get('correo', '').strip()

        # Estructura de decisión: verificar que no esté vacío
        if not correo:
            raise forms.ValidationError('El correo electrónico es un campo obligatorio.')

        # Validador de formato de correo estándar de Django
        validador_email = EmailValidator(message='Por favor, ingrese un formato de correo electrónico válido (ejemplo: usuario@dominio.com).')
        validador_email(correo)

        return correo