# Generated by Django 3.2.13 on 2022-05-18 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0019_hardware'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hardware',
            name='picture',
            field=models.ImageField(null=True, upload_to='picture'),
        ),
    ]