# Generated by Django 3.0.5 on 2020-12-03 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='identifier',
            field=models.CharField(default='c5f12ac352303e08ca1b', max_length=300, verbose_name='Identificador'),
        ),
    ]