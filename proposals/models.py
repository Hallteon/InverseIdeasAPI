import uuid
import datetime
from django.db import models
from django_currentuser.db.models import CurrentUserField
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Status(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    status_type = models.CharField(max_length=255, verbose_name='Тип статуса')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class History(models.Model):
    by_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='histories_user', verbose_name='Пользователь')
    status = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='histories_status', verbose_name='Статус')
    date = models.DateTimeField(default=datetime.datetime.now(), blank=True, verbose_name='Дата')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    
    def __str__(self):
        return f'{self.date} - {self.by_user}'
    
    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'Истории'


class Proposal(models.Model):
    def get_path(instance, filename):
        pdf_uuid = uuid.uuid1().hex

        return f'proposals/documents/{pdf_uuid}.pdf'
    
    name = models.CharField(max_length=255, verbose_name='Название')
    author = CurrentUserField(verbose_name='Автор')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='proposals_category', verbose_name='Категория')
    content = models.JSONField(verbose_name='Содержание')
    document = models.FileField(upload_to=get_path, verbose_name='Файл документа')
    histories = models.ManyToManyField('History', blank=True, related_name='proposals_history', verbose_name='История')
    level = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(3)], verbose_name='Уровень')
    created_date = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Дата создания')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'