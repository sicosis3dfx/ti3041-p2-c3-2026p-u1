from django import forms
from django.core.validators import EmailValidator
from .models import Contacto


# Formulario vinculado al modelo Contacto para registrar y editar
class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        # Los 4 campos requeridos en la evaluación
        fields = ['nombre', 'telefono', 'correo', 'direccion']
        labels = {
            'nombre': 'Nombre completo',
            'telefono': 'Teléfono',
            'correo': 'Correo electrónico',
            'direccion': 'Dirección',
        }
        # Widgets para asignar clases css y placeholders a los inputs
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej. María González', 'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'placeholder': '1234 5678', 'class': 'form-control', 'maxlength': '12'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'nombre@ejemplo.com', 'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Calle, número y comuna', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si se está editando un contacto, mostramos solo los 8 dígitos en el input porque el prefijo +56 9 ya se muestra visualmente
        if self.instance and self.instance.pk and self.instance.telefono:
            tel = self.instance.telefono
            for prefijo in ['+56 9', '+569', '569']:
                if tel.startswith(prefijo):
                    tel = tel[len(prefijo):].strip()
                    break
            self.initial['telefono'] = tel

    def clean_telefono(self):
        # Validación de teléfono: prefijo +569 y exactamente 8 dígitos numéricos
        telefono = self.cleaned_data.get('telefono', '').strip()

        if not telefono:
            raise forms.ValidationError('El teléfono es obligatorio.')

        # Si el usuario ingresó el prefijo, lo quitamos para analizar los dígitos
        for prefijo in ['+56 9', '+569', '569']:
            if telefono.startswith(prefijo):
                telefono = telefono[len(prefijo):].strip()
                break

        # Quitamos espacios y guiones para quedarnos con los números
        digitos = telefono.replace(' ', '').replace('-', '')

        # Validamos que sean únicamente números
        if not digitos.isdigit():
            raise forms.ValidationError('El teléfono debe contener solo números.')

        # Validamos que sean exactamente 8 dígitos
        if len(digitos) != 8:
            raise forms.ValidationError('El teléfono debe tener exactamente 8 dígitos después del prefijo (+56 9).')

        # Guardamos el formato estándar: +56 9 XXXX XXXX
        return f"+56 9 {digitos[:4]} {digitos[4:]}"

    def clean_correo(self):
        # Validación del correo antes de guardar
        correo = self.cleaned_data.get('correo', '').strip()

        # Si viene vacío o con puros espacios, lanzamos error
        if not correo:
            raise forms.ValidationError('El correo electrónico es obligatorio.')

        # Usamos el EmailValidator de Django para revisar que tenga formato correcto (usuario@dominio)
        validador_email = EmailValidator(message='Ingresa un correo válido con formato correcto (ej: usuario@dominio.com).')
        validador_email(correo)

        return correo