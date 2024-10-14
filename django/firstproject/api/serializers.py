from rest_framework.serializers import ModelSerializer

from men.models import Men

# Класс MenSerializer наследуется от ModelSerializer, который предоставляет удобный способ сериализации и десериализации объектов модели.
class MenSerializer(ModelSerializer):
    class Meta:
        # Указываем модель, которую будем сериализовать. В данном случае это модель Men.
        model = Men
        
        # Указываем, что будем сериализовать все поля модели.
        fields = "__all__"
