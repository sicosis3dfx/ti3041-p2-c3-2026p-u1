import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html

from .forms import ContactoForm
from .models import Contacto

from django.contrib.admin.actions import delete_selected

# Personalización de títulos del panel de administración
admin.site.site_header = "Agenda de Contactos - Panel de Control"
admin.site.site_title = "Agenda Contactos Admin"
admin.site.index_title = "Gestión y Administración de Contactos"

# Texto en español para la acción de borrado masivo por defecto
delete_selected.short_description = "🗑️ Eliminar contactos seleccionados"


@admin.action(description="📥 Exportar contactos seleccionados a CSV")
def exportar_contactos_csv(modeladmin, request, queryset):
    """Acción masiva para descargar contactos en archivo CSV compatible con Excel."""
    response = HttpResponse(
        content_type='text/csv; charset=utf-8-sig',
        headers={'Content-Disposition': 'attachment; filename="contactos_exportados.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Teléfono', 'Correo electrónico', 'Dirección'])
    for c in queryset:
        writer.writerow([c.id, c.nombre, c.telefono, c.correo, c.direccion])
    return response


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    # Formulario con validaciones de teléfono chileno y correo
    form = ContactoForm

    # Columnas con enlaces interactivos
    list_display = ('nombre', 'enlace_telefono', 'enlace_correo', 'direccion')

    # Búsqueda simultánea
    search_fields = ('nombre', 'correo', 'telefono')

    # Orden predeterminado
    ordering = ('nombre',)

    # Paginación
    list_per_page = 20

    # Acciones masivas
    actions = [exportar_contactos_csv]

    @admin.display(description="Teléfono", ordering='telefono')
    def enlace_telefono(self, obj):
        if not obj.telefono:
            return "-"
        numero_limpio = obj.telefono.replace(' ', '')
        return format_html(
            '<a href="tel:{}" class="badge-telefono">'
            '📞 <span>{}</span></a>',
            numero_limpio,
            obj.telefono,
        )

    @admin.display(description="Correo electrónico", ordering='correo')
    def enlace_correo(self, obj):
        if not obj.correo:
            return "-"
        return format_html(
            '<a href="mailto:{}" class="badge-correo">'
            '✉️ <span>{}</span></a>',
            obj.correo,
            obj.correo,
        )
