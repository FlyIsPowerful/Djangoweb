# Generated by Django 3.2.13 on 2022-04-28 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0007_rename_username_info_usernames'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthy',
            name='time',
            field=models.CharField(max_length=20, null=True),
        ),
    ]