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
]