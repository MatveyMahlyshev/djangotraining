import requests
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from men.models import Men
from api.serializers import MenSerializer
from api.filters import MenFilter
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import status


# Класс MenViewSet наследуется от ModelViewSet, который предоставляет полный набор CRUD-операций для модели.
class MenViewSet(ModelViewSet):
    # Указываем сериализатор, который будет использоваться для преобразования объектов модели в JSON и обратно.
    serializer_class = MenSerializer
    
    # Указываем queryset, который будет использоваться для получения данных из базы данных.
    queryset = Men.objects.all()
    
    # Указываем класс пагинации, который будет использоваться для разбиения результатов на страницы.
    pagination_class = PageNumberPagination
    
    # Указываем список бэкендов фильтрации, которые будут использоваться для фильтрации, сортировки и поиска данных.
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    
    # Указываем класс фильтра, который будет использоваться для фильтрации данных.
    filterset_class = MenFilter
    
    # Указываем, что сортировка будет применяться ко всем полям модели.
    ordering_fields = '__all__'
    
    # Указываем поля, по которым будет производиться поиск. В данном случае это поле "title".
    search_fields = ["title"]




User = get_user_model()

class GenderizeView(APIView):
    def get(self, request, format=None):
        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        # Получаем имя из query параметра или используем имя пользователя
        name = request.query_params.get('name', request.user.first_name)

        # Если имя все еще не определено, возвращаем ошибку
        if not name:
            return Response({"error": "Name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Формируем URL для запроса к Genderize API
        url = f"https://api.genderize.io/?name={name}"
        response = requests.get(url)

        if response.status_code == 200:
            # Можно добавить имя пользователя в ответ
            data = response.json()
            data['username'] = request.user.first_name

            # Обновляем поле gender в модели User
            user = request.user
            user.gender = data['gender']
            user.save()

            return Response(data)
        else:
            return Response({"error": "Failed to fetch data from Genderize API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)