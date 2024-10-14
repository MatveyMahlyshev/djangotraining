import unittest
from django.test import TestCase, Client
from django.urls import reverse
from men.models import Men, Comment, Category
from users.models import User  

class TestAddComment(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Тестовая категория', slug='test-category')
        self.post = Men.objects.create(title='Тестовая запись', content='Содержание записи', slug='test-post', cat=self.category)
        self.url = reverse('add_comment', kwargs={'post_slug': self.post.slug})
        self.comment_data = {'text': 'Это тестовый комментарий'}
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_add_comment(self):
        self.client.login(username='testuser', password='testpassword')  # Аутентификация пользователя
        response = self.client.post(self.url, self.comment_data)
        self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление после успешного добавления комментария
        self.assertTrue(Comment.objects.filter(text='Это тестовый комментарий').exists())  # Проверяем, что комментарий был добавлен

    def tearDown(self):
        self.post.delete()
        self.category.delete()
        self.user.delete()