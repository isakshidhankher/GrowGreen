# Generated by Django 3.1 on 2022-01-11 17:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0012_auto_20220111_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 11, 22, 36, 37, 95011)),
        ),
    ]
