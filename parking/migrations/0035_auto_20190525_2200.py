# Generated by Django 2.1.7 on 2019-05-26 02:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0034_auto_20190525_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arriendo',
            name='end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='arriendo',
            name='price',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='arriendo',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 25, 22, 0, 24, 246956)),
        ),
    ]
