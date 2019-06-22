# Generated by Django 2.1.7 on 2019-04-19 18:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parking', '0018_remove_rol_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='rol',
            name='granted_to',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]