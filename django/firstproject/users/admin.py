# Импортируем необходимые модули Django для работы с административной панелью
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Импортируем модель User из текущего приложения
from .models import User

# Регистрируем модель User в административной панели Django
# Используем класс UserAdmin для настройки отображения и функционала модели User в админке
admin.site.register(User, UserAdmin)