# Generated by Django 3.0.5 on 2020-11-24 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20201121_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='identifier',
            field=models.CharField(default='4e3567fdbfade0460c62', max_length=300, verbose_name='Identificador'),
        ),
    ]
