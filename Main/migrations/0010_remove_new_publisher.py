# Generated by Django 3.2.13 on 2022-05-05 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0009_new'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='new',
            name='publisher',
        ),
    ]