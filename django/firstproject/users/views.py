from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
import requests

from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm

# Класс для представления страницы входа пользователя
class LoginUser(LoginView):
    # Используем нашу форму для входа
    form_class = LoginUserForm
    # Указываем шаблон для отображения
    template_name = 'users/login.html'
    # Дополнительный контекст для передачи в шаблон
    extra_context = {'title': 'Авторизация'}

# Класс для представления страницы регистрации нового пользователя
class RegisterUser(CreateView):
    # Используем нашу форму для регистрации
    form_class = RegisterUserForm
    # Указываем шаблон для отображения
    template_name = 'users/register.html'
    # Дополнительный контекст для передачи в шаблон
    extra_context = {'title': 'Регистрация'}
    # Указываем URL для перенаправления после успешной регистрации
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # Сохраняем форму, чтобы получить объект пользователя
        response = super().form_valid(form)
        user = self.object

        # Получаем имя пользователя из поля first_name
        first_name = user.first_name

        if first_name:
            # Формируем URL для запроса к Genderize API
            url = f"https://api.genderize.io/?name={first_name}"
            genderize_response = requests.get(url)

            if genderize_response.status_code == 200:
                # Получаем данные о поле из ответа API
                gender_data = genderize_response.json()
                gender = gender_data.get('gender')

                if gender:
                    # Обновляем поле gender в модели User
                    user.gender = gender
                    user.save()

        return response

# Класс для представления страницы профиля пользователя
class ProfileUser(LoginRequiredMixin, UpdateView):
    # Используем модель пользователя
    model = get_user_model()
    # Используем нашу форму для редактирования профиля
    form_class = ProfileUserForm
    # Указываем шаблон для отображения
    template_name = 'users/profile.html'
    # Дополнительный контекст для передачи в шаблон
    extra_context = {'title': 'Профиль пользователя'}

    # Метод для получения URL для перенаправления после успешного обновления профиля
    def get_success_url(self):
        return reverse_lazy('users:profile')

    # Метод для получения объекта пользователя, который будет редактироваться
    def get_object(self, queryset=None):
        return self.request.user

# Класс для представления страницы изменения пароля пользователя
class UserPasswordChange(PasswordChangeView):
    # Используем нашу форму для изменения пароля
    form_class = UserPasswordChangeForm
    # Указываем URL для перенаправления после успешного изменения пароля
    success_url = reverse_lazy('users:password_change_done')
    # Указываем шаблон для отображения
    template_name = 'users/password_change_form.html'