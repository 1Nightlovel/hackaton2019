# Generated by Django 2.1.7 on 2019-04-15 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0009_auto_20190404_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='NumVerification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tel', models.CharField(max_length=8)),
                ('code', models.CharField(max_length=4)),
                ('success', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='user_comp_data',
            name='username2',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
