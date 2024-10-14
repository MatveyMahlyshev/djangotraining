from rest_framework.test import APITestCase
from rest_framework import status
from men.models import Men, Category

class MenViewSetTests(APITestCase):

    def setUp(self):
        # Создаем тестовые данные для связанной модели Category
        self.category1 = Category.objects.create(name="Category 1", slug="category-1")
        self.category2 = Category.objects.create(name="Category 2", slug="category-2")

        # Создаем несколько тестовых объектов для тестирования
        self.men1 = Men.objects.create(title="Man 1", content="Content 1", cat=self.category1)
        self.men2 = Men.objects.create(title="Man 2", content="Content 2", cat=self.category1)
        self.men3 = Men.objects.create(title="Man 3", content="Content 3", cat=self.category2)

    def test_list_men(self):
        """
        Тестирование получения списка всех объектов Men.
        """
        response = self.client.get('/api/men/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Directly access response.data as a list

    def test_create_men(self):
        """
        Тестирование создания нового объекта Men.
        """
        data = {'title': 'New Man', 'content': 'New Content', 'cat': self.category1.id}
        response = self.client.post('/api/men/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Men.objects.count(), 4)
        self.assertEqual(Men.objects.get(id=response.data['id']).title, 'New Man')

    def test_retrieve_men(self):
        """
        Тестирование получения конкретного объекта Men.
        """
        response = self.client.get(f'/api/men/{self.men1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.men1.title)

    def test_update_men(self):
        """
        Тестирование обновления объекта Men.
        """
        data = {'title': 'Updated Man', 'content': 'Updated Content', 'cat': self.category2.id}
        response = self.client.put(f'/api/men/{self.men1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.men1.refresh_from_db()
        self.assertEqual(self.men1.title, 'Updated Man')
        self.assertEqual(self.men1.cat, self.category2)

    def test_delete_men(self):
        """
        Тестирование удаления объекта Men.
        """
        response = self.client.delete(f'/api/men/{self.men1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Men.objects.count(), 2)

    def test_filter_men(self):
        """
        Тестирование фильтрации объектов Men.
        """
        response = self.client.get('/api/men/?title=Man 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Directly access response.data as a list
        self.assertEqual(response.data[0]['title'], 'Man 1')

    def test_search_men(self):
        """
        Тестирование поиска объектов Men.
        """
        response = self.client.get('/api/men/?search=Man 2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Directly access response.data as a list
        self.assertEqual(response.data[0]['title'], 'Man 2')

    def test_ordering_men(self):
        """
        Тестирование сортировки объектов Men.
        """
        response = self.client.get('/api/men/?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Man 1')  # Directly access response.data as a list
        self.assertEqual(response.data[1]['title'], 'Man 2')
        self.assertEqual(response.data[2]['title'], 'Man 3')

        response = self.client.get('/api/men/?ordering=-title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Man 3')  # Directly access response.data as a list
        self.assertEqual(response.data[1]['title'], 'Man 2')
        self.assertEqual(response.data[2]['title'], 'Man 1')