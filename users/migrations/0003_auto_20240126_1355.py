# Generated by Django 3.2.23 on 2024-01-26 08:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20240125_1133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='achievement',
            name='total_progress',
        ),
        migrations.AddField(
            model_name='achievementtype',
            name='total_progress',
            field=models.IntegerField(default=0, verbose_name='Прогресс всего'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='birthday',
            field=models.DateField(default=datetime.date(2024, 1, 26), verbose_name='День рождения'),
        ),
    ]
