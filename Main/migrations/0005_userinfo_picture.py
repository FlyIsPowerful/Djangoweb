# Generated by Django 3.2.13 on 2022-04-25 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0004_rename_password_healthy_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='picture',
            field=models.ImageField(default='avatar3.jpg', upload_to='picture'),
        ),
    ]
