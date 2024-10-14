from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

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