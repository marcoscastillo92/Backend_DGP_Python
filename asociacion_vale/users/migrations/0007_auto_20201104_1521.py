# Generated by Django 3.0.5 on 2020-11-04 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20201104_1510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(default='20257386825af244242ca7d945384ac36f6541b8e2f19bf7d3ff76b2740998cd3af8e84f7bf674562912c1dab42a99d377bf2883f0a50e2e0c4b880a499eb432', max_length=300),
        ),
    ]
