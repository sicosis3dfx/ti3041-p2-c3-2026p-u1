from django.db import models


# Modelo para guardar los contactos de la agenda
class Contacto(models.Model):
    # Campos que nos pide el enunciado para cada contacto
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    telefono = models.CharField(max_length=30, verbose_name="Teléfono")
    correo = models.EmailField(max_length=254, verbose_name="Correo electrónico")
    direccion = models.CharField(max_length=200, verbose_name="Dirección")

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        # Ordenamos la lista por nombre en orden alfabético
        ordering = ['nombre']

    def __str__(self):
        # Para que al imprimir o mostrar el objeto se vea el nombre y no 'Contacto object (id)'
        return self.nombre