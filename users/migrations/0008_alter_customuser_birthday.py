# Generated by Django 3.2.23 on 2024-01-17 08:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20240117_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birthday',
            field=models.DateField(default=datetime.date(2024, 1, 17), verbose_name='День рождения'),
        ),
    ]
