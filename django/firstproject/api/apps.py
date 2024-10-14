from django.apps import AppConfig

# Класс ApiConfig наследуется от AppConfig, который предоставляет Django информацию о конфигурации приложения.
class ApiConfig(AppConfig):
    # Устанавливаем значение по умолчанию для поля 'id' в моделях приложения как BigAutoField.
    # Это поле будет автоматически генерироваться для каждой записи в базе данных.
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Указываем имя приложения, которое будет использоваться Django для его идентификации.
    # В данном случае, это приложение называется 'api'.
    name = 'api'