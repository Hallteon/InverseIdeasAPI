# Generated by Django 3.2.23 on 2024-01-17 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0002_auto_20240117_1322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='date',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='created_date',
        ),
    ]
