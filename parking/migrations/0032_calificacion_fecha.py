# Generated by Django 2.1.7 on 2019-05-25 23:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0031_calificacion_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='calificacion',
            name='fecha',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
