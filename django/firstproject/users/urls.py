from django.contrib.auth.views import LogoutView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy
from . import views

# Указываем пространство имен для приложения
app_name = 'users'

# Определяем маршруты для приложения
urlpatterns = [
    # Маршрут для страницы входа
    path('login/', views.LoginUser.as_view(), name='login'),
    
    # Маршрут для выхода пользователя из системы
    path('logout/', LogoutView.as_view(), name='logout'),

    # Маршрут для изменения пароля авторизованного пользователя
    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    
    # Маршрут для страницы подтверждения смены пароля
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'), name='password_change_done'),

    # Маршрут для восстановления пароля через email
    path('password-reset/',
         PasswordResetView.as_view(
             template_name='users/password_reset_form.html',
             email_template_name='users/password_reset_email.html',
             success_url=reverse_lazy('users:password_reset_done'),
         ),
         name='password_reset'),
    
    # Маршрут для страницы с дальнейшими инструкциями для восстановления пароля
    path('password-reset/done', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    
    # Маршрут для отправки одноразовой ссылки восстановления пароля на email
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html',
             success_url=reverse_lazy('users:password_reset_complete'),
         ),
         name='password_reset_confirm'),

    # Маршрут для страницы успешной смены пароля через email
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    
    # Маршрут для страницы регистрации нового пользователя
    path('register/', views.RegisterUser.as_view(), name='register'),
    
    # Маршрут для страницы профиля пользователя
    path('profile/', views.ProfileUser.as_view(), name='profile')
]