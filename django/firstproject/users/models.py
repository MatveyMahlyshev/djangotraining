from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Поле для загрузки фотографии пользователя
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True, verbose_name='Фото')
    
    # Поле для хранения даты рождения пользователя
    date_of_birth = models.DateTimeField(blank=True, null=True, verbose_name='Дата Рождения')
    
    # Поле для хранения пола пользователя
    gender = models.CharField(max_length=10, blank=True, null=True, verbose_name='Пол')