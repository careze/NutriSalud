# Generated by Django 5.0.4 on 2024-06-21 17:27

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('hipertension', 'Hipertensión'), ('celiaco', 'Celíaco'), ('obeso', 'Obeso'), ('renal', 'Renal'), ('diabetico', 'Diabético'), ('ninguno', 'Ninguno')], max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('foto', models.ImageField(upload_to='fotos_comida/')),
                ('nombreMenu', models.CharField(max_length=255)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('descripcion', models.TextField()),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Crud.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('foto', models.ImageField(upload_to='fotos_comida/')),
                ('nombreProducto', models.CharField(max_length=255)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('marca', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Crud.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='correo electrónico')),
                ('nombre', models.CharField(max_length=30)),
                ('apellido', models.CharField(max_length=30)),
                ('edad', models.IntegerField()),
                ('telefono', models.CharField(max_length=15)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Crud.categoria')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Corazon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_crear', models.DateTimeField(auto_now_add=True)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='Crud.menu')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('menu', 'user')},
            },
        ),
    ]
