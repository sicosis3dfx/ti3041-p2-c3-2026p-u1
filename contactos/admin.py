from django.contrib import admin
from .forms import ContactoForm
from .models import Contacto

# Personalización de títulos del panel de administración
admin.site.site_header = "Agenda de Contactos - Panel de Control"
admin.site.site_title = "Agenda Contactos Admin"
admin.site.index_title = "Gestión y Administración de Contactos"


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    # Formulario personalizado que incluye las validaciones de teléfono y correo
    form = ContactoForm

    # Columnas que se mostrarán en la tabla del panel
    list_display = ('nombre', 'telefono', 'correo', 'direccion')

    # Campos por los que se puede buscar en el panel
    search_fields = ('nombre', 'correo', 'telefono')

    # Orden predeterminado alfabético por nombre
    ordering = ('nombre',)

    # Cantidad de contactos por página
    list_per_page = 20
