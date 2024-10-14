from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import MenViewSet, GenderizeView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Создаем экземпляр DefaultRouter, который автоматически генерирует URL-маршруты для ViewSet.
router = DefaultRouter()

# Регистрируем MenViewSet с маршрутом 'men'.
# Это позволяет автоматически создавать URL-маршруты для действий CRUD.
router.register(r'men', MenViewSet, basename='men')

# Создаем экземпляр schema_view для Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Your API",
      default_version='v1',
      description="BLOG API",
      terms_of_service="https://www.yourapp.com/terms/",
      contact=openapi.Contact(email="contact@yourapp.com"),
      license=openapi.License(name="Your License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# Определяем URL-шаблоны для нашего приложения.
urlpatterns = [
    # Включаем URL-маршруты, сгенерированные DefaultRouter, в путь 'api/'.
    path('api/', include(router.urls)),
    path('api/genderize/', GenderizeView.as_view(), name='genderize'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]