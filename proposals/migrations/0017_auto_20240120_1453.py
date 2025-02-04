# Generated by Django 3.2.23 on 2024-01-20 09:53

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proposals', '0016_auto_20240119_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 20, 14, 53, 31, 891837), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='history',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 1, 20, 14, 53, 31, 889761), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='author',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='proposals_author', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 20, 14, 53, 31, 890392), verbose_name='Дата создания'),
        ),
    ]
