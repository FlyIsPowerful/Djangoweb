# Generated by Django 3.2.13 on 2022-05-05 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0008_healthy_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='New',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, null=True)),
                ('content', models.CharField(max_length=200, null=True)),
                ('publisher', models.CharField(max_length=3, null=True)),
                ('time', models.CharField(max_length=20, null=True)),
            ],
        ),
    ]