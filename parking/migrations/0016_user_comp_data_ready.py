# Generated by Django 2.1.7 on 2019-04-19 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0015_auto_20190418_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_comp_data',
            name='ready',
            field=models.BooleanField(default=False),
        ),
    ]