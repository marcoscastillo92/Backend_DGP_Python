# Generated by Django 3.0.5 on 2020-11-16 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20201116_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='identifier',
            field=models.CharField(default='ff8a99d218318b075a31', max_length=300, verbose_name='Identificador'),
        ),
    ]
