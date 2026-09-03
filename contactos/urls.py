from django.urls import path
from . import views

# Rutas de la aplicación de Agenda de Contactos (Caso 3)
urlpatterns = [
    # Listado general de contactos y búsqueda por nombre o correo
    path('', views.contacto_list, name='contacto_list'),
    # Formulario para registrar un nuevo contacto
    path('contactos/nuevo/', views.contacto_create, name='contacto_create'),
    # Vista detallada de un contacto por su clave primaria (pk)
    path('contactos/<int:pk>/', views.contacto_detail, name='contacto_detail'),
    # Formulario para actualizar/editar la información de un contacto
    path('contactos/<int:pk>/editar/', views.contacto_update, name='contacto_update'),
    # Confirmación y eliminación de un contacto
    path('contactos/<int:pk>/eliminar/', views.contacto_delete, name='contacto_delete'),
]