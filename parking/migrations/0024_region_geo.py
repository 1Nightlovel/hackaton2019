# Generated by Django 2.1.7 on 2019-05-07 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0023_auto_20190425_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='geo',
            field=models.FileField(null=True, upload_to='geo'),
        ),
    ]
