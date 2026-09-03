from django.test import TestCase
from django.urls import reverse

from .forms import ContactoForm
from .models import Contacto


class ContactoViewsTest(TestCase):
    """
    Pruebas unitarias para validar el cumplimiento de los requerimientos del Caso 3:
    1. Agregar contactos con nombre, teléfono, correo y dirección.
    2. Buscar contactos por nombre o correo.
    3. Validar formato de correo electrónico.
    """

    def setUp(self):
        self.contacto = Contacto.objects.create(
            nombre="Juan Perez",
            telefono="+56 9 1234 5678",
            correo="juan@example.com",
            direccion="Av. Siempre Viva 123",
        )
        self.contacto2 = Contacto.objects.create(
            nombre="Maria Lopez",
            telefono="+56 9 8765 4321",
            correo="maria@servidor.cl",
            direccion="Calle Los Olivos 456",
        )

    def test_contacto_create_valido(self):
        """Requerimiento: Agregar contactos con datos válidos."""
        datos = {
            'nombre': 'Carlos Soto',
            'telefono': '+56 9 1111 2222',
            'correo': 'carlos@empresa.com',
            'direccion': 'Pasaje Central 789',
        }
        response = self.client.post(reverse('contacto_create'), data=datos)
        self.assertRedirects(response, reverse('contacto_list'))
        self.assertTrue(Contacto.objects.filter(correo='carlos@empresa.com').exists())

    def test_validar_formato_correo_invalido(self):
        """Requerimiento: Validar formato de correo electrónico (rechazar si es incorrecto)."""
        form = ContactoForm(data={
            'nombre': 'Pedro Prueba',
            'telefono': '+56 9 0000 0000',
            'correo': 'correo-invalido-sin-arroba',
            'direccion': 'Dirección de prueba',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('correo', form.errors)

    def test_validar_formato_correo_valido(self):
        """Requerimiento: Validar formato de correo electrónico (aceptar si cumple formato)."""
        form = ContactoForm(data={
            'nombre': 'Ana Gomez',
            'telefono': '+56 9 9999 8888',
            'correo': 'ana.gomez@dominio.cl',
            'direccion': 'Avenida Prat 100',
        })
        self.assertTrue(form.is_valid())

    def test_buscar_contacto_por_nombre(self):
        """Requerimiento: Buscar contactos por nombre."""
        response = self.client.get(reverse('contacto_list'), {'q': 'Juan'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Perez')
        self.assertNotContains(response, 'Maria Lopez')

    def test_buscar_contacto_por_correo(self):
        """Requerimiento: Buscar contactos por correo."""
        response = self.client.get(reverse('contacto_list'), {'q': 'maria@servidor.cl'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Lopez')
        self.assertNotContains(response, 'Juan Perez')

    def test_contacto_create_does_not_show_delete_button(self):
        response = self.client.get(reverse('contacto_create'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Eliminar contacto")

    def test_contacto_update_shows_delete_button(self):
        url = reverse('contacto_update', args=[self.contacto.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        delete_url = reverse('contacto_delete', args=[self.contacto.pk])
        self.assertContains(response, "Eliminar contacto")
        self.assertContains(response, delete_url)

    def test_contacto_delete_view(self):
        delete_url = reverse('contacto_delete', args=[self.contacto.pk])
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"¿Eliminar a {self.contacto.nombre}?")

        post_response = self.client.post(delete_url)
        self.assertRedirects(post_response, reverse('contacto_list'))
        self.assertFalse(Contacto.objects.filter(pk=self.contacto.pk).exists())

