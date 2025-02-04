# Generated by Django 3.2.23 on 2024-01-24 09:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0017_auto_20240120_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='description',
            field=models.TextField(default='', verbose_name='Описание'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 24, 14, 53, 14, 638953), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='history',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 1, 24, 14, 53, 14, 637431), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 24, 14, 53, 14, 637910), verbose_name='Дата создания'),
        ),
    ]
