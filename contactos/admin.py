import csv
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.admin.actions import delete_selected

from .forms import ContactoForm
from .models import Contacto

# ==============================================================================
# 1. Branding del Panel de Administración (Clase 02U2 - Sección 7)
# ==============================================================================
admin.site.site_header = "Agenda de Contactos - Panel de Control"
admin.site.site_title = "Agenda Contactos Admin"
admin.site.index_title = "Gestión y Administración de Contactos"

# Personalización del texto para la acción por defecto de borrado
delete_selected.short_description = "🗑️ Eliminar contactos seleccionados"


# ==============================================================================
# 2. Acciones Masivas Personalizadas (Clase 02U2 - Sección 3)
# ==============================================================================
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


@admin.action(description="✨ Estandarizar nombres seleccionados (Mayúscula inicial)")
def estandarizar_nombres(modeladmin, request, queryset):
    """
    Acción masiva que estandariza la capitalización de los nombres seleccionados
    y notifica al usuario con un mensaje en el panel.
    """
    actualizados = 0
    for contacto in queryset:
        nombre_limpio = ' '.join(contacto.nombre.strip().split()).title()
        if contacto.nombre != nombre_limpio:
            contacto.nombre = nombre_limpio
            contacto.save(update_fields=['nombre'])
            actualizados += 1

    modeladmin.message_user(
        request,
        f"Se han estandarizado los nombres de {actualizados} contacto(s) correctamente."
    )


# ==============================================================================
# 3. Filtros Avanzados Personalizados (Clase 02U2 - Sección 4)
# ==============================================================================
class ProveedorCorreoFilter(SimpleListFilter):
    """Filtro avanzado lateral para clasificar contactos según su proveedor de correo electrónico."""
    title = 'Proveedor de correo'
    parameter_name = 'proveedor'

    def lookups(self, request, model_admin):
        return (
            ('gmail', 'Gmail (@gmail.com)'),
            ('inacap', 'Institucional INACAP (@inacap.cl / @inacapmail.cl)'),
            ('outlook', 'Microsoft / Outlook / Hotmail'),
            ('otros', 'Otros proveedores'),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'gmail':
            return queryset.filter(correo__icontains='@gmail.com')
        if val == 'inacap':
            return queryset.filter(correo__icontains='@inacap.cl') | queryset.filter(correo__icontains='@inacapmail.cl')
        if val == 'outlook':
            return queryset.filter(correo__icontains='@outlook.') | queryset.filter(correo__icontains='@hotmail.')
        if val == 'otros':
            return queryset.exclude(
                correo__icontains='@gmail.com'
            ).exclude(
                correo__icontains='@inacap'
            ).exclude(
                correo__icontains='@outlook.'
            ).exclude(
                correo__icontains='@hotmail.'
            )
        return queryset


# ==============================================================================
# 4. Configuración Principal del Modelo en Admin (Clase 02U2 - Secciones 2, 5 y 6)
# ==============================================================================
@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    # Formulario personalizado con validaciones específicas
    form = ContactoForm

    # Visualización en lista
    list_display = ('nombre', 'enlace_telefono', 'enlace_correo', 'direccion')

    # Búsqueda rápida por múltiples campos
    search_fields = ('nombre', 'correo', 'telefono')

    # Filtros laterales (incluyendo el SimpleListFilter personalizado)
    list_filter = (ProveedorCorreoFilter,)

    # Ordenamiento por defecto
    ordering = ('nombre',)

    # Paginación
    list_per_page = 20

    # Acciones masivas registradas
    actions = [exportar_contactos_csv, estandarizar_nombres]

    # Agrupación visual de campos en secciones (Fieldsets & UX)
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre',),
            'description': 'Datos principales de identificación del contacto.',
        }),
        ('Canales de Comunicación', {
            'fields': ('telefono', 'correo'),
            'description': 'Canales directos para establecer contacto telefónico o digital.',
        }),
        ('Ubicación y Domicilio', {
            'fields': ('direccion',),
            'classes': ('collapse',),
            'description': 'Información física del contacto (sección colapsable).',
        }),
    )

    # Lógica de guardado y auditoría desde el admin
    def save_model(self, request, obj, form, change):
        """Limpia espacios en blanco antes de guardar el modelo desde el Admin."""
        if obj.nombre:
            obj.nombre = ' '.join(obj.nombre.strip().split())
        if obj.direccion:
            obj.direccion = ' '.join(obj.direccion.strip().split())
        super().save_model(request, obj, form, change)

    # Control de permisos por rol
    def has_delete_permission(self, request, obj=None):
        """Solo los superusuarios tienen permiso para eliminar contactos desde el panel."""
        return bool(request.user and request.user.is_superuser)

    # Personalización en español de las opciones del menú de acciones
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            func, name, _ = actions['delete_selected']
            actions['delete_selected'] = (func, name, "🗑️ Eliminar contactos seleccionados")
        return actions

    def get_action_choices(self, request, default_choices=None):
        default_choices = [("", "- Selecciona una opción -")]
        return super().get_action_choices(request, default_choices=default_choices)

    # Decoradores de visualización interactiva
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

# ==============================================================================
# 5. Personalizaci?n del Modelo de Usuarios (Diferenciaci?n de Roles Visuales)
# ==============================================================================
if admin.site.is_registered(User):
    admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    # Reemplazamos la columna gen?rica 'is_staff' por nuestro badge descriptivo de Rol
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol_badge', 'is_active')
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'groups')
    ordering = ('username',)

    @admin.display(description="Rol / Nivel de acceso", ordering='is_superuser')
    def rol_badge(self, obj):
        """Muestra visualmente si el usuario es Superusuario, Staff o Usuario estándar."""
        if obj.is_superuser:
            return mark_safe(
                '<span class="badge-role badge-superuser">👑 Superusuario</span>'
            )
        elif obj.is_staff:
            return mark_safe(
                '<span class="badge-role badge-staff">🛡️ Staff</span>'
            )
        else:
            return mark_safe(
                '<span class="badge-role badge-user">👤 Usuario normal</span>'
            )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            func, name, _ = actions['delete_selected']
            actions['delete_selected'] = (func, name, "🗑️ Eliminar usuarios seleccionados")
        return actions

    def get_action_choices(self, request, default_choices=None):
        default_choices = [("", "- Selecciona una opción -")]
        return super().get_action_choices(request, default_choices=default_choices)

