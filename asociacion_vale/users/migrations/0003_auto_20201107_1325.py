# Generated by Django 3.0.2 on 2020-11-07 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20201107_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(default='39f49b26dfeecae6bce50015ca13d8950a4af98413d4b602ba62e0ae14df2fabe5653afde38641e873592b3495638354613c998586540ca98cf0da08698d33ee', max_length=300),
        ),
    ]
