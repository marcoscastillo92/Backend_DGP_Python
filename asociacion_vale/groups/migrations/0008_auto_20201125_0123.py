# Generated by Django 3.0.5 on 2020-11-25 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0007_auto_20201124_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='identifier',
            field=models.CharField(default='74ca05188a1a9a174bd5', max_length=300, verbose_name='Identificador'),
        ),
    ]