# Generated by Django 3.0.5 on 2020-12-03 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='identifier',
            field=models.CharField(default='90dc3641a8fab6f6aa96', max_length=300, verbose_name='Identificador'),
        ),
    ]