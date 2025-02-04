import datetime
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class AchievementType(models.Model):
    def get_path(instance, filename):
        extension = filename.split('.')[-1]
        image_uuid = uuid.uuid1().hex

        return f'users/achievements/{image_uuid}.{extension}'
    
    cover = models.ImageField(blank=True, null=True, upload_to=get_path, verbose_name='Обложка')
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    points = models.IntegerField(verbose_name='Баллы')
    achievement_type_name = models.CharField(max_length=255, verbose_name='Тип')
    total_progress = models.IntegerField(default=0, verbose_name='Прогресс всего')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тип достижения'
        verbose_name_plural = 'Типы достижений'


class Achievement(models.Model):
    achievement_type = models.ForeignKey('AchievementType', on_delete=models.CASCADE, 
                                         related_name='achievements_achievementtype', verbose_name='Тип')
    current_progress = models.IntegerField(default=0, verbose_name='Прогресс сейчас')    
    
    def __str__(self):
        return f'{self.achievement_type.name} - {self.current_progress}'
    
    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'


class Job(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.CharField(max_length=255, verbose_name='Описание')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class Role(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    role_type = models.CharField(max_length=255, verbose_name='Тип поли')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email,  phone_number='8 902-277-41-85', telegram='@Hallteon',
                          firstname='Иван', lastname='Белогуров', surname='Дмитриевич',
                          job=Job.objects.get(pk=1), role=Role.objects.get(pk=3), password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    def get_path(instance, filename):
        extension = filename.split('.')[-1]
        image_uuid = uuid.uuid1().hex

        return f'users/avatars/{image_uuid}.{extension}'
    
    email = models.EmailField(unique=True, blank=True, verbose_name='Почта')
    avatar = models.ImageField(blank=True, null=True, upload_to=get_path, verbose_name='Аватар')
    phone_number = models.CharField(max_length=255, blank=True, unique=True, verbose_name='Номер телефона')
    telegram = models.CharField(max_length=255, unique=True, verbose_name='Телеграм')
    firstname = models.CharField(max_length=255, verbose_name='Имя')
    lastname = models.CharField(max_length=255, verbose_name='Фамилия')
    surname = models.CharField(max_length=255, verbose_name='Отчество')
    birthday = models.DateField(default=datetime.date.today(), verbose_name='День рождения')
    job = models.ForeignKey('Job', default=1, null=True, on_delete=models.CASCADE, related_name='users_job', verbose_name='Должность')
    achievements = models.ManyToManyField('Achievement', related_name='users_achievement', verbose_name='Достижения')
    role = models.ForeignKey('Role', default=2, on_delete=models.CASCADE, related_name='users_role', verbose_name='Роль')
    password = models.CharField(max_length=255, verbose_name='Пароль')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'