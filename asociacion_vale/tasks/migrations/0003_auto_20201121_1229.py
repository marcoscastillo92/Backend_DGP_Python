# Generated by Django 3.0.5 on 2020-11-21 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('tasks', '0002_auto_20201119_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='identifier',
            field=models.CharField(default='822b4117da1ca33fbcb8', max_length=300, verbose_name='Identificador'),
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('done', models.BooleanField(default=False)),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.Task', verbose_name='Tarea')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.User', verbose_name='Usuario')),
            ],
        ),
    ]
