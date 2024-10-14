# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import MenViewSet, GenderizeView

# Создаем экземпляр DefaultRouter, который автоматически генерирует URL-маршруты для ViewSet.
router = DefaultRouter()

# Регистрируем MenViewSet с маршрутом 'men'.
# Это позволяет автоматически создавать URL-маршруты для действий CRUD.
router.register(r'men', MenViewSet, basename='men')

# Определяем URL-шаблоны для нашего приложения.
urlpatterns = [
    # Включаем URL-маршруты, сгенерированные DefaultRouter, в путь 'api/'.
    path('api/', include(router.urls)),
    path('api/genderize/', GenderizeView.as_view(), name='genderize')
    
]