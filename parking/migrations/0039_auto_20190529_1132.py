# Generated by Django 2.1.7 on 2019-05-29 15:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0038_auto_20190525_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arriendo',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 29, 15, 32, 23, 48997, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='calificacion',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2019, 5, 29, 15, 32, 23, 48997, tzinfo=utc)),
        ),
    ]
