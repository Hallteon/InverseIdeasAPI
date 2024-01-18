import datetime
from django.db import models
from users.models import CustomUser


class Office(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    creation_date = models.DateField(default=datetime.date.today(), verbose_name='Дата создрания')
    address = models.TextField(verbose_name='Адрес')
    heads = models.ManyToManyField(CustomUser, related_name='offices_head', verbose_name='Руководители')
    departments = models.ManyToManyField('Department', blank=True, related_name='offices_department', verbose_name='Департаменты')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Офис'
        verbose_name_plural = 'Офисы'


class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='ОПисание')
    heads = models.ManyToManyField(CustomUser, related_name='departments_head', verbose_name='Руководители')
    divisions = models.ManyToManyField('Division', blank=True, related_name='departments_division', verbose_name='Отделы')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'


class Division(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    employees = models.ManyToManyField(CustomUser, blank=True, related_name='divisions_employee', verbose_name='Сотрудники')
    heads = models.ManyToManyField(CustomUser, related_name='divisions_head', verbose_name='Руководители')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'