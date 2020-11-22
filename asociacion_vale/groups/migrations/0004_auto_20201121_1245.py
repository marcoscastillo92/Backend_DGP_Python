# Generated by Django 3.0.5 on 2020-11-21 11:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0003_auto_20201121_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='tutors',
            field=models.ManyToManyField(blank=True, related_name='tutores', to=settings.AUTH_USER_MODEL, verbose_name='Tutores'),
        ),
        migrations.AlterField(
            model_name='groups',
            name='identifier',
            field=models.CharField(default='686d45947ea5d62ba1a6', max_length=300, verbose_name='Identificador'),
        ),
    ]