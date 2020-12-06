# Generated by Django 3.0.5 on 2020-12-02 19:27

import ckeditor.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', ckeditor.fields.RichTextField(verbose_name='Mensaje')),
                ('mimeType', models.FileField(blank=True, upload_to='uploads/attach', verbose_name='Tipo de mensaje')),
                ('createdAt', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Fecha de creacion')),
                ('category', models.CharField(max_length=200, verbose_name='Categoria Mensaje')),
                ('identifier', models.CharField(max_length=300, verbose_name='Identificador')),
                ('emisorTutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emisorTutor', to=settings.AUTH_USER_MODEL, verbose_name='Emisor Tutor')),
                ('emisorUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emisorUser', to='users.User', verbose_name='Emisor Usuario')),
                ('receptorTutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receptorTutor', to=settings.AUTH_USER_MODEL, verbose_name='Receptor Tutor')),
                ('receptorUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receptorUser', to='users.User', verbose_name='Receptor Usuario')),
            ],
            options={
                'verbose_name': 'Mensaje',
                'verbose_name_plural': 'Mensajes',
            },
        ),
    ]
