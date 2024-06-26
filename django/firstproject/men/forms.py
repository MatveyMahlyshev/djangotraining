from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Wife


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийкламнопрстуфхцшщъыьэюя-1234567890 '
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Должны присутствовать только руссие символы, дефис и пробел.'

    def __call__(self, value, *args, **kwargs):
        if not(set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=5,
                            label='Заголовок:',
                            widget=forms.TextInput(attrs={'class': 'form-input'}),
                            error_messages={
                                'min_length': 'Слишком короткий заголовок',
                                'required': 'Без заголовка никак',
                            })
    slug = forms.SlugField(max_length=255, label='Слаг:',
                           validators=[
                               MinLengthValidator(5, message='Слишком короткий слаг.'),
                               MaxLengthValidator(100),
                           ]
                           )
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Текст:', )
    is_published = forms.BooleanField(required=False, label='Публикация:', initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория:',
                                 empty_label='Категория не выбрана')
    wife = forms.ModelChoiceField(queryset=Wife.objects.all(), required=False, label='Супруга:', empty_label='Не женат')

    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийкламнопрстуфхцшщъыьэюя-1234567890 '
        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError('Должны присутствовать только руссие символы, дефис и пробел.')