# Generated by Django 3.0.5 on 2020-11-25 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20201124_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='identifier',
            field=models.CharField(default='6f35e92086a732d6a834', max_length=300, verbose_name='Identificador'),
        ),
    ]
