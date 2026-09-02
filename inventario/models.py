from django.db import models

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30)
    correo = models.EmailField(max_length=254)
    direccion = models.CharField(max_length=200)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre