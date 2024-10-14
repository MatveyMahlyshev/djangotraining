from django.contrib.auth.models import Group

# Обработчик для нового пользователя, который выполняется после успешной аутентификации через социальную сеть
def new_user_handler(backend, user, response, *args, **kwargs):
    # Ищем группу с именем 'social'
    group = Group.objects.filter(name='social')
    
    # Если группа существует, добавляем пользователя в эту группу
    if len(group):
        user.groups.add(group[0])