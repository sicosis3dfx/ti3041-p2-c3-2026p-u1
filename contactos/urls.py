from django.urls import path
from . import views

# Rutas de la app contactos
urlpatterns = [
    # Página principal: lista de contactos y buscador
    path('', views.contacto_list, name='contacto_list'),
    # Formulario para agregar un contacto
    path('contactos/nuevo/', views.contacto_create, name='contacto_create'),
    # Ver la información completa de un contacto según su ID
    path('contactos/<int:pk>/', views.contacto_detail, name='contacto_detail'),
    # Formulario para editar un contacto existente
    path('contactos/<int:pk>/editar/', views.contacto_update, name='contacto_update'),
    # Confirmar y eliminar un contacto
    path('contactos/<int:pk>/eliminar/', views.contacto_delete, name='contacto_delete'),
    # Confirmar y eliminar múltiples contactos seleccionados
    path('contactos/eliminar-multiples/', views.contacto_bulk_delete, name='contacto_bulk_delete'),
    # Integración móvil vCard (.vcf)
    path('contactos/<int:pk>/vcard/', views.contacto_vcard_download, name='contacto_vcard_download'),
    path('contactos/exportar-vcard/', views.contactos_vcard_export_all, name='contactos_vcard_export_all'),
    path('contactos/exportar-seleccionados/', views.contactos_vcard_export_selected, name='contactos_vcard_export_selected'),
    path('contactos/importar-vcard/', views.contacto_vcard_import, name='contacto_vcard_import'),
]
