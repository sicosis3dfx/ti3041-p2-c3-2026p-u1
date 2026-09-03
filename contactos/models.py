from django.db import models


class Contacto(models.Model):
    """
    Modelo que representa a un Contacto Personal (Caso 3: Agenda de Contactos Personal).
    Almacena los datos requeridos: nombre, teléfono, correo electrónico y dirección.
    """
    # Identificación y datos de contacto según especificación
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    telefono = models.CharField(max_length=30, verbose_name="Teléfono")
    correo = models.EmailField(max_length=254, verbose_name="Correo electrónico")
    direccion = models.CharField(max_length=200, verbose_name="Dirección")

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        ordering = ['nombre']

    def __str__(self):
        """Representación textual del contacto en listas y panel de administración."""
        return self.nombre