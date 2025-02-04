# Generated by Django 3.2.23 on 2024-01-19 07:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proposals', '0011_auto_20240118_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Содержание')),
                ('created_datetime', models.DateTimeField(default=datetime.datetime(2024, 1, 19, 12, 22, 31, 707718), verbose_name='Дата создания')),
                ('author', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
            },
        ),
        migrations.AlterField(
            model_name='history',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 1, 19, 12, 22, 31, 706127), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 19, 12, 22, 31, 706578), verbose_name='Дата создания'),
        ),
        migrations.CreateModel(
            name='ProposalPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.IntegerField(default=0, verbose_name='Лайки')),
                ('views', models.IntegerField(default=0, verbose_name='Просмотры')),
                ('comments', models.ManyToManyField(related_name='proposalposts_comment', to='proposals.Comment', verbose_name='Комментарии')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposalposts_proposal', to='proposals.proposal', verbose_name='Заявка')),
                ('tags', models.ManyToManyField(related_name='proposalposts_tag', to='proposals.Tag', verbose_name='Тэги')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
            },
        ),
    ]
