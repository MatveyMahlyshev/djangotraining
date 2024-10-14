from django_filters import rest_framework as filters
from men.models import Men
from django.db import models

# Класс MenFilter наследуется от filters.FilterSet, который предоставляет возможность фильтрации данных в Django REST Framework.
class MenFilter(filters.FilterSet):
    class Meta:
        # Указываем модель, к которой будет применяться фильтрация. В данном случае это модель Men.
        model = Men
        
        # Указываем, что фильтрация будет применяться ко всем полям модели.
        fields = '__all__'
        
        # Переопределяем фильтры для определенных типов полей.
        filter_overrides = {
            # Для полей типа models.ImageField будет применяться фильтр CharFilter.
            models.ImageField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {
                    # Указываем, что фильтрация будет происходить с учетом регистра (icontains).
                    'lookup_expr': 'icontains',
                },
            },
        }