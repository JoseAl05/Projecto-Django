# Generated by Django 3.2.7 on 2021-09-13 14:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='gender',
            field=models.CharField(default='Hombre', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2021, 9, 13, 11, 30, 0, 22355), verbose_name='Fecha de Registro'),
        ),
    ]
