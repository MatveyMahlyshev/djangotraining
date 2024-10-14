menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
]

# Класс DataMixin предоставляет общие данные и методы для использования в представлениях.
class DataMixin:
    title_page = None  # Заголовок страницы.
    cat_selected = None  # Выбранная категория.
    extra_context = {}  # Дополнительный контекст для передачи в шаблон.
    paginate_by = 2  # Количество элементов на странице при пагинации.

    # Конструктор класса, который инициализирует дополнительный контекст.
    def __init__(self):
        # Если заголовок страницы указан, добавляем его в контекст.
        if self.title_page:
            self.extra_context['title'] = self.title_page

        # Если меню еще не добавлено в контекст, добавляем его.
        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

        # Если выбрана категория, добавляем ее в контекст.
        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected

    # Метод get_mixin_context обновляет контекст данными из миксина.
    def get_mixin_context(self, context, **kwargs):
        # Добавляем меню в контекст.
        context['menu'] = menu
        
        # Устанавливаем значение по умолчанию для выбранной категории.
        context['cat_selected'] = None
        
        # Обновляем контекст переданными аргументами.
        context.update(**kwargs)
        
        # Возвращаем обновленный контекст.
        return context