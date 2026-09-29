from django.apps import AppConfig


class ContactosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contactos'
    verbose_name = 'Agenda de Contactos'

    def ready(self):
        # Estandarizamos en español la etiqueta por defecto de los selects en Django
        from django.db.models import fields
        fields.BLANK_CHOICE_LABEL = "- Selecciona una opción -"

