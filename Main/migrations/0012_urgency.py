# Generated by Django 3.2.13 on 2022-05-09 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0011_rename_time_new_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='urgency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=20, null=True)),
                ('content', models.CharField(max_length=100, null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
            ],
        ),
    ]