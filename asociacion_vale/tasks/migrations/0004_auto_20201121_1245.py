# Generated by Django 3.0.5 on 2020-11-21 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20201121_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='identifier',
            field=models.CharField(default='9e8ae6e2a001f72959ea', max_length=300, verbose_name='Identificador'),
        ),
    ]
