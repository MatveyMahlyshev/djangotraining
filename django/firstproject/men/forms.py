from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from men.models import Comment

from .models import Category, Wife, Men

# Декоратор deconstructible позволяет сохранять пользовательские валидаторы при миграции.
@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийкламнопрстуфхцшщъыьэюя-1234567890 '
    code = 'russian'

    # Метод clean_title выполняет валидацию поля title.
    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийкламнопрстуфхцшщъыьэюя-1234567890 '
        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError('Должны присутствовать только русские символы, дефис и пробел.')

    # Конструктор класса, позволяющий передавать сообщение об ошибке.
    def __init__(self, message=None):
        self.message = message if message else 'Должны присутствовать только руссие символы, дефис и пробел.'

    # Метод __call__ выполняет валидацию значения.
    def __call__(self, value, *args, **kwargs):
        if not(set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


# Класс AddPostForm наследуется от forms.ModelForm, который предоставляет удобный способ создания форм на основе моделей.
class AddPostForm(forms.ModelForm):
    # Поле cat позволяет выбрать категорию из списка всех категорий.
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория:', empty_label='Категория не выбрана')
    
    # Поле wife позволяет выбрать супругу из списка всех супруг.
    wife = forms.ModelChoiceField(queryset=Wife.objects.all(), required=False, label='Супруга:', empty_label='Не женат')

    class Meta:
        model = Men  # Указываем модель, на основе которой создается форма.
        fields = ['title', 'content', 'photo', 'is_published', 'cat', 'wife', 'tags']  # Указываем поля, которые будут отображаться в форме.
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),  # Указываем виджет для поля title.
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),  # Указываем виджет для поля content.
        }

    # Метод clean_title выполняет валидацию поля title.
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов.')
        return title



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'comment-input', 'rows': 2}),
        }

# Класс UploadFileForm наследуется от forms.Form, который предоставляет удобный способ создания форм без привязки к модели.
class UploadFileForm(forms.Form):
    file = forms.FileField(label='Файл')  # Поле file позволяет загружать файлы.