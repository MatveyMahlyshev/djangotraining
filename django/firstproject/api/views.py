from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from men.models import Men
from api.serializers import MenSerializer
from api.filters import MenFilter

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