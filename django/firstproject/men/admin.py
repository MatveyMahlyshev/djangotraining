from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Men, Category, TagPost, Wife

# Класс MarriedFilter наследуется от admin.SimpleListFilter, который позволяет создавать собственные фильтры для админки.
class MarriedFilter(admin.SimpleListFilter):
    title = 'Статус мужчин'  # Заголовок фильтра.
    parameter_name = 'status'  # Параметр, который будет использоваться в URL для фильтрации.

    # Метод lookups возвращает список кортежей, где первый элемент — значение параметра, а второй — отображаемое имя.
    def lookups(self, request, model_admin):
        return [
            ('married', 'Женат'),
            ('single', 'Не женат')
        ]

    # Метод queryset возвращает отфильтрованный queryset на основе значения параметра.
    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(wife__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(wife__isnull=True)


# Регистрируем модель Men в админке с помощью декоратора @admin.register.
@admin.register(Men)
class MenAdmin(admin.ModelAdmin):
    # Указываем поля, которые будут отображаться в форме редактирования/создания записи.
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'tags', 'wife']
    
    # Указываем поля, которые будут доступны только для чтения.
    readonly_fields = ['post_photo']
    
    # Указываем поля, которые будут отображаться в списке записей.
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat', 'slug')
    
    # Указываем поля, которые будут ссылками на страницу редактирования записи.
    list_display_links = ('title',)
    
    # Указываем порядок сортировки записей по умолчанию.
    ordering = ['time_create', 'title']
    
    # Указываем поля, которые можно редактировать прямо в списке записей.
    list_editable = ('is_published',)
    
    # Указываем количество записей на одной странице.
    list_per_page = 10
    
    # Указываем действия, которые можно выполнять над выбранными записями.
    actions = ['set_published', 'set_draft']
    
    # Указываем поля, по которым будет производиться поиск.
    search_fields = ['title__startswith', 'cat__name']
    
    # Указываем фильтры, которые будут отображаться в админке.
    list_filter = [MarriedFilter, 'cat__name', 'is_published']
    
    # Указываем, что кнопки сохранения должны отображаться вверху страницы.
    save_on_top = True

    # Метод post_photo отображает фотографию записи.
    @admin.display(description='Фото')
    def post_photo(self, men: Men):
        if men.photo:
            return mark_safe(f'<img src="{men.photo.url}" width=50>')
        else:
            return 'Без фото'

    # Действие set_published публикует выбранные записи.
    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Men.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записей.')

    # Действие set_draft снимает выбранные записи с публикации.
    @admin.action(description='Снять выбранные записи из публикации')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Men.Status.DRAFT)
        self.message_user(request, f'Изменено {count} записей.', messages.WARNING)


# Регистрируем модель Category в админке.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    ordering = ['id']


# Регистрируем модель TagPost в админке.
@admin.register(TagPost)
class TapPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'slug')
    list_display_links = ('id', 'tag')
    ordering = ['id']


# Регистрируем модель Wife в админке.
@admin.register(Wife)
class WifeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age')
    list_display_links = ('id', 'name')
    ordering = ['id']