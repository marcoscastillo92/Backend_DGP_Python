# Generated by Django 3.0.2 on 2020-11-07 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_auto_20201107_1417'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forumgroup',
            old_name='grupo',
            new_name='Group',
        ),
    ]