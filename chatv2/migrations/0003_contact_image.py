# Generated by Django 3.1 on 2022-01-11 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatv2', '0002_auto_20211224_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='image',
            field=models.ImageField(default='/media/triangle.jpg', null=True, upload_to='user_images'),
        ),
    ]
