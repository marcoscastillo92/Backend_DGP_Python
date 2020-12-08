# Generated by Django 3.0.5 on 2020-12-08 09:24

import datetime
from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pictograms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('key', models.CharField(max_length=300)),
                ('section', models.CharField(max_length=150)),
                ('image', models.ImageField(default='null', upload_to=users.models.pictogram_directory_path, verbose_name='Imagen de Pictograma')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre y Apellidos')),
                ('email', models.CharField(max_length=150, verbose_name='Correo Electrónico')),
                ('username', models.CharField(max_length=150, verbose_name='Nombre de Usuario')),
                ('password', models.CharField(max_length=150, verbose_name='Contraseña')),
                ('phoneNumber', models.CharField(max_length=150, verbose_name='Número de Teléfono')),
                ('profileImage', models.ImageField(blank=True, upload_to=users.models.user_directory_path, verbose_name='Imagen de Perfil')),
                ('birthDate', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Nacimiento')),
                ('token', models.CharField(default='null', max_length=300)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=6, verbose_name='Sexo')),
                ('createdAt', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('deviceToken', models.CharField(default='', max_length=300, verbose_name='TokenDispositivo')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
    ]
