# Generated by Django 3.0.2 on 2020-11-07 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('groups', '0002_auto_20201107_1215'),
        ('forums', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Message',
            new_name='MessageForum',
        ),
    ]