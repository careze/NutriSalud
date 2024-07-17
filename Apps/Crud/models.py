import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Categoria(models.Model):
    CATEGORIAS_CHOICES = [
        ('hipertension', 'Hipertensión'),
        ('celiaco', 'Celíaco'),
        ('obeso', 'Obeso'),
        ('renal', 'Renal'),
        ('diabetico', 'Diabético'),
        ('ninguno', 'Ninguno'),
    ]
    nombre = models.CharField(max_length=50, choices=CATEGORIAS_CHOICES, unique=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    foto = models.ImageField(upload_to='fotos_comida/')
    nombreProducto = models.CharField(max_length=255)
    categoria = models.ManyToManyField(Categoria)
    precio = models.IntegerField()
    marca = models.CharField(max_length=100)
    descripcion = models.TextField()
    stock = models.IntegerField(default=0)

    
    def __str__(self):
        return self.nombreProducto

class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    foto = models.ImageField(upload_to='fotos_comida/')
    nombreMenu = models.CharField(max_length=255)
    categoria = models.ManyToManyField(Categoria)
    precio = models.IntegerField()
    descripcion = models.TextField()
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.nombreMenu

class Corazon(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_crear = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('menu', 'user')

class Carrito(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='CarritoProducto')

class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def total_precio(self):
        return self.cantidad * self.precio

class UserManager(BaseUserManager):
    def create_user(self, email, nombre, apellido, edad, telefono, password=None, categoria=None):
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico")
        user = self.model(
            email=self.normalize_email(email),
            nombre=nombre,
            apellido=apellido,
            edad=edad,
            telefono=telefono,
            categoria=categoria
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, apellido, edad, telefono, password=None, categoria=None):
        user = self.create_user(
            email,
            nombre=nombre,
            apellido=apellido,
            edad=edad,
            telefono=telefono,
            password=password,
            categoria=categoria
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='correo electrónico', max_length=255, unique=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    edad = models.IntegerField()
    telefono = models.CharField(max_length=15)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()  # creación de usuarios.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'edad', 'telefono']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
