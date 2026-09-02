from django.test import TestCase
from django.urls import reverse

from .models import Contacto


class ContactoViewsTest(TestCase):
    def setUp(self):
        self.contacto = Contacto.objects.create(
            nombre="Juan Perez",
            telefono="+56 9 1234 5678",
            correo="juan@example.com",
            direccion="Av. Siempre Viva 123",
        )

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
