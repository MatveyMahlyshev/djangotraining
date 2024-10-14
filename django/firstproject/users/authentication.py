# Импортируем необходимые модули Django для работы с аутентификацией
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

# Создаем собственный бэкенд аутентификации, который позволяет аутентифицировать пользователей по email
class EmailAuthBackend(BaseBackend):
    # Метод authenticate вызывается при попытке аутентификации пользователя
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Получаем модель пользователя
        user_model = get_user_model()
        try:
            # Пытаемся найти пользователя по email (который передается как username)
            user = user_model.objects.get(email=username)
            # Проверяем, совпадает ли пароль
            if user.check_password(password):
                return user
            # Если пароль не совпадает, возвращаем None
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            # Если пользователь не найден или найдено несколько пользователей с таким email, возвращаем None
            return None

    # Метод get_user используется для получения пользователя по его ID
    def get_user(self, user_id):
        # Получаем модель пользователя
        user_model = get_user_model()
        try:
            # Пытаемся найти пользователя по его ID
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            # Если пользователь не найден, возвращаем None
            return None