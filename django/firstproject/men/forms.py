from django import forms
from .models import Category, Wife


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label='Заголовок:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    slug = forms.SlugField(max_length=255, label='Слаг:')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Текст:', )
    is_published = forms.BooleanField(required=False, label='Публикация:', initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория:',
                                 empty_label='Категория не выбрана')
    wife = forms.ModelChoiceField(queryset=Wife.objects.all(), required=False, label='Супруга:', empty_label='Не женат')
