from django.contrib.auth.models import AbstractUser
from django.db import models

# Расширяем стандартную модель пользователя Django, добавляя дополнительные поля
class User(AbstractUser):
    # Поле для загрузки фотографии пользователя
    # upload_to указывает путь для сохранения файлов, %Y/%m/%d будет заменено на текущую дату
    # blank=True позволяет сохранять пустое значение, null=True позволяет базе данных хранить NULL
    # verbose_name задает человекочитаемое название поля
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True, verbose_name='Фото')
    
    # Поле для хранения даты рождения пользователя
    # blank=True позволяет сохранять пустое значение, null=True позволяет базе данных хранить NULL
    # verbose_name задает человекочитаемое название поля
    date_of_birth = models.DateTimeField(blank=True, null=True, verbose_name='Дата Рождения')