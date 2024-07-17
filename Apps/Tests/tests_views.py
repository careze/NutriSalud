# Tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from Apps.Crud.models import Producto  # Actualiza la importación del modelo Producto

class HomeViewTests(TestCase):

    def test_cargarInicio_view_status_code(self):
        url = reverse('cargarInicio')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_cargarproducto_view_status_code(self):
        url = reverse('cargarproducto')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_cargarmenu_view_status_code(self):
        url = reverse('cargarmenu')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_cargarcontacto_view_status_code(self):
        url = reverse('cargarcontacto')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_cargarpreguntas_view_status_code(self):
        url = reverse('cargarpreguntas')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_cargarsomos_view_status_code(self):
        url = reverse('cargarsomos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_cargarcarro_view_status_code(self):
        url = reverse('cargarcarro')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_view_status_code(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_registro_view_status_code(self):
        url = reverse('registro')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_templates_used(self):
        templates = [
            ('cargarInicio', '0_base.html'),
            ('cargarproducto', '2_productos.html'),
            ('cargarmenu', '3_menus.html'),
            ('cargarcontacto', '4_contacto.html'),
            ('cargarpreguntas', '5_preguntas.html'),
            ('cargarsomos', '6_nosotros.html'),
            ('cargarcarro', '7_carro.html'),
            ('login', '8_sesiones.html'),
            ('registro', 'registro.html')
        ]
        for url_name, template in templates:
            with self.subTest(url_name=url_name):
                url = reverse(url_name)
                response = self.client.get(url)
                self.assertTemplateUsed(response, template)
