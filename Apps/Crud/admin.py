from django.contrib import admin
from .models import Categoria, User, Producto, Menu

admin.site.register(Categoria)
admin.site.register(User)
admin.site.register(Producto)
admin.site.register(Menu)