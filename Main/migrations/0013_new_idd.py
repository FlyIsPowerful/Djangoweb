# Generated by Django 3.2.13 on 2022-05-09 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0012_urgency'),
    ]

    operations = [
        migrations.AddField(
            model_name='new',
            name='idd',
            field=models.IntegerField(max_length=2, null=True),
        ),
    ]
