# Apps/Tests/test_producto.py
from django.test import TestCase
from Apps.Crud.models import Producto, Categoria  # Ajusta según la estructura de tu proyecto

class ProductoModelTests(TestCase):

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='diabetico')
    
    def test_creacion_producto(self):
        producto = Producto.objects.create(
            nombreProducto='Producto de Prueba',
            precio=10,
            descripcion='Descripción del producto de prueba',
            marca='Marca de Prueba'
        )
        producto.categoria.add(self.categoria)
        self.assertEqual(producto.nombreProducto, 'Producto de Prueba')
        self.assertEqual(producto.precio, 10)
        self.assertEqual(producto.descripcion, 'Descripción del producto de prueba')
        self.assertEqual(producto.marca, 'Marca de Prueba')

    def test_metodo_str_producto(self):
        producto = Producto.objects.create(
            nombreProducto='Producto de Prueba',
            precio=10,
            descripcion='Descripción del producto de prueba',
            marca='Marca de Prueba'
        )
        self.assertEqual(str(producto), 'Producto de Prueba')

    def test_actualizacion_precio_producto(self):
        producto = Producto.objects.create(
            nombreProducto='Producto de Prueba',
            precio=10,
            descripcion='Descripción del producto de prueba',
            marca='Marca de Prueba'
        )
        producto.precio = 15
        producto.save()
        self.assertEqual(producto.precio, 15)

    def test_eliminacion_producto(self):
        producto = Producto.objects.create(
            nombreProducto='Producto de Prueba',
            precio=10,
            descripcion='Descripción del producto de prueba',
            marca='Marca de Prueba'
        )
        producto_id = producto.id
        producto.delete()
        with self.assertRaises(Producto.DoesNotExist):
            Producto.objects.get(id=producto_id)
