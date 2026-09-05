from django.test import TestCase
from django.urls import reverse

from .forms import ContactoForm
from .models import Contacto


# Pruebas unitarias para verificar que todo funcione correctamente
class ContactoViewsTest(TestCase):

    def setUp(self):
        # Creamos dos contactos de prueba en la base de datos temporal
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
        # Probamos guardar un nuevo contacto con datos correctos
        datos = {
            'nombre': 'Carlos Soto',
            'telefono': '+56 9 1111 2222',
            'correo': 'carlos@empresa.com',
            'direccion': 'Pasaje Central 789',
        }
        response = self.client.post(reverse('contacto_create'), data=datos)
        # Debe redirigir a la lista y el contacto debe existir en la BD
        self.assertRedirects(response, reverse('contacto_list'))
        self.assertTrue(Contacto.objects.filter(correo='carlos@empresa.com').exists())

    def test_validar_formato_correo_invalido(self):
        # Probamos que el formulario rechace un correo sin formato correcto (sin @ ni dominio)
        form = ContactoForm(data={
            'nombre': 'Pedro Prueba',
            'telefono': '+56 9 0000 0000',
            'correo': 'correo-invalido-sin-arroba',
            'direccion': 'Dirección de prueba',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('correo', form.errors)

    def test_validar_formato_correo_valido(self):
        # Probamos que el formulario acepte un correo con estructura válida
        form = ContactoForm(data={
            'nombre': 'Ana Gomez',
            'telefono': '+56 9 9999 8888',
            'correo': 'ana.gomez@dominio.cl',
            'direccion': 'Avenida Prat 100',
        })
        self.assertTrue(form.is_valid())

    def test_validar_telefono_valido_solo_8_digitos(self):
        # Probamos que el formulario acepte ingresar los 8 dígitos directamente
        form = ContactoForm(data={
            'nombre': 'Lucas Mora',
            'telefono': '87654321',
            'correo': 'lucas@correo.cl',
            'direccion': 'Calle Nueva 123',
        })
        self.assertTrue(form.is_valid())
        # Verificamos que se guarde con el prefijo +56 9
        self.assertEqual(form.cleaned_data['telefono'], '+56 9 8765 4321')

    def test_validar_telefono_invalido_menos_de_8_digitos(self):
        # Probamos que rechace números con menos de 8 dígitos
        form = ContactoForm(data={
            'nombre': 'Lucas Mora',
            'telefono': '12345',
            'correo': 'lucas@correo.cl',
            'direccion': 'Calle Nueva 123',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)

    def test_validar_telefono_invalido_con_letras(self):
        # Probamos que rechace teléfonos con letras
        form = ContactoForm(data={
            'nombre': 'Lucas Mora',
            'telefono': '1234abcd',
            'correo': 'lucas@correo.cl',
            'direccion': 'Calle Nueva 123',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)

    def test_buscar_contacto_por_nombre(self):
        # Probamos que el buscador filtre por nombre
        response = self.client.get(reverse('contacto_list'), {'q': 'Juan'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Perez')
        self.assertNotContains(response, 'Maria Lopez')

    def test_buscar_contacto_por_correo(self):
        # Probamos que el buscador filtre por correo
        response = self.client.get(reverse('contacto_list'), {'q': 'maria@servidor.cl'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Lopez')
        self.assertNotContains(response, 'Juan Perez')

    def test_contacto_create_does_not_show_delete_button(self):
        # Al crear un contacto nuevo no debe aparecer el botón de eliminar
        response = self.client.get(reverse('contacto_create'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Eliminar contacto")

    def test_contacto_update_shows_delete_button(self):
        # Al editar un contacto existente sí debe aparecer la opción de eliminar
        url = reverse('contacto_update', args=[self.contacto.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        delete_url = reverse('contacto_delete', args=[self.contacto.pk])
        self.assertContains(response, "Eliminar contacto")
        self.assertContains(response, delete_url)

    def test_contacto_delete_view(self):
        # Probamos la confirmación y eliminación de un contacto
        delete_url = reverse('contacto_delete', args=[self.contacto.pk])
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"¿Eliminar a {self.contacto.nombre}?")

        # Enviamos la petición POST para confirmar el borrado
        post_response = self.client.post(delete_url)
        self.assertRedirects(post_response, reverse('contacto_list'))
        self.assertFalse(Contacto.objects.filter(pk=self.contacto.pk).exists())

    def test_contacto_bulk_delete_get_redirects(self):
        # Acceder por GET directo a bulk_delete debe redirigir a la lista
        response = self.client.get(reverse('contacto_bulk_delete'))
        self.assertRedirects(response, reverse('contacto_list'))

    def test_contacto_bulk_delete_empty_selection_redirects(self):
        # Enviar POST sin selección debe redirigir a la lista sin borrar nada
        response = self.client.post(reverse('contacto_bulk_delete'), data={'selected_ids': []})
        self.assertRedirects(response, reverse('contacto_list'))
        self.assertEqual(Contacto.objects.count(), 2)

    def test_contacto_bulk_delete_shows_confirmation(self):
        # Enviar POST con IDs debe mostrar la pantalla de confirmación con los nombres
        response = self.client.post(
            reverse('contacto_bulk_delete'),
            data={'selected_ids': [self.contacto.pk, self.contacto2.pk]}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "¿Eliminar 2 contactos?")
        self.assertContains(response, self.contacto.nombre)
        self.assertContains(response, self.contacto2.nombre)

    def test_contacto_bulk_delete_confirmed_deletes_records(self):
        # Enviar confirmación definitiva debe borrar los registros seleccionados
        response = self.client.post(
            reverse('contacto_bulk_delete'),
            data={
                'selected_ids': [self.contacto.pk, self.contacto2.pk],
                'confirmar': '1',
            }
        )
        self.assertRedirects(response, reverse('contacto_list'))
        # Ambos contactos fueron eliminados
        self.assertFalse(Contacto.objects.filter(pk=self.contacto.pk).exists())
        self.assertFalse(Contacto.objects.filter(pk=self.contacto2.pk).exists())
        self.assertEqual(Contacto.objects.count(), 0)


