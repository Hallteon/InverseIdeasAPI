# Generated by Django 3.2.23 on 2024-01-18 08:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0009_auto_20240117_1356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='comment',
        ),
        migrations.AlterField(
            model_name='history',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 1, 18, 13, 50, 50, 703654), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 18, 13, 50, 50, 704114), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='histories',
            field=models.ManyToManyField(blank=True, related_name='proposals_history', to='proposals.History', verbose_name='История'),
        ),
    ]
