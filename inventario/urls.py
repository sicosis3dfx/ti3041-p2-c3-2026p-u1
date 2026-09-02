from django.urls import path
from .import views

urlpatterns = [
    path('', views.contacto_list, name='contacto_list'),
    path('contactos/nuevo/', views.contacto_create, name='contacto_create'),
    path('contactos/<int:pk>/', views.contacto_detail, name='contacto_detail'),
    path('contactos/<int:pk>/editar/', views.contacto_update, name='contacto_update'),
    path('contactos/<int:pk>/eliminar/', views.contacto_delete, name='contacto_delete'),
]