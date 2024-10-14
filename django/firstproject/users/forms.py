import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError

# Форма для входа пользователя
class LoginUserForm(AuthenticationForm):
    # Поле для ввода логина с настройками виджета и класса CSS
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    # Поле для ввода пароля с настройками виджета и класса CSS
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        # Используем модель пользователя, которая определена в проекте
        model = get_user_model()
        # Указываем поля, которые будут отображаться в форме
        fields = ['username', 'password']

# Форма для регистрации нового пользователя
class RegisterUserForm(UserCreationForm):
    # Поле для ввода логина с настройками виджета и класса CSS
    username = forms.CharField(label='Логин',  widget=forms.TextInput(attrs={'class': 'form-input'}))
    # Поле для ввода пароля с настройками виджета и класса CSS
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}), )
    # Поле для повторного ввода пароля с настройками виджета и класса CSS
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        # Используем модель пользователя, которая определена в проекте
        model = get_user_model()
        # Указываем поля, которые будут отображаться в форме
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        # Устанавливаем метки для полей формы
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        # Настраиваем виджеты для полей формы
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    # Метод для валидации email
    def clean_email(self):
        email = self.cleaned_data['email']
        # Проверяем, существует ли уже пользователь с таким email
        if get_user_model().objects.filter(email=email).exists():
            # Если существует, выбрасываем ошибку валидации
            raise ValidationError('Данный e-mail адрес уже зарегистрирован.')
        return email

# Форма для редактирования профиля пользователя
class ProfileUserForm(forms.ModelForm):
    # Поле для отображения логина (нередактируемое)
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # Поле для отображения email (нередактируемое, необязательное)
    email = forms.CharField(disabled=True, required=False, label='Почта',
                            widget=forms.TextInput(attrs={'class': 'form-input'}))
    # Получаем текущий год для настройки выбора даты рождения
    this_year = datetime.date.today().year
    # Поле для выбора даты рождения с настройками виджета
    date_of_birth = forms.DateTimeField(widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5))))

    class Meta:
        # Используем модель пользователя, которая определена в проекте
        model = get_user_model()
        # Указываем поля, которые будут отображаться в форме
        fields = ['photo', 'username', 'email', 'date_of_birth', 'first_name', 'last_name']
        # Устанавливаем метки для полей формы
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        # Настраиваем виджеты для полей формы
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

# Форма для изменения пароля пользователя
class UserPasswordChangeForm(PasswordChangeForm):
    # Поле для ввода старого пароля с настройками виджета и класса CSS
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'text-input'}))
    # Поле для ввода нового пароля с настройками виджета и класса CSS
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'text-input'}))
    # Поле для повторного ввода нового пароля с настройками виджета и класса CSS
    new_password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'text-input'}))