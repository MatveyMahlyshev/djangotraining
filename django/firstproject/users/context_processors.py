# Импортируем функцию menu из модуля utils приложения men
from men.utils import menu

# Функция get_men_context возвращает контекст для шаблона, содержащий меню
def get_men_context(request):
    # Возвращаем словарь с ключом 'mainmenu', значением которого является переменная menu
    return {'mainmenu': menu}