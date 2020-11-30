from django.test import TestCase
# Импортирование НАШЕЙ модели Post
from .models import Post 
# Импортирование стандартной модели Django User
from django.contrib.auth import get_user_model

from django.urls import reverse 


# Create your tests here.

class SimpleBlogTests(TestCase):
    """
    Класс для тестирования общего функционала приложения
    Включает в себя:
    1) setUp :
           Определяем пользователя и добавляем его в тестовую БД
           Определим пост, созданный тестовым пользователем
    2) test_str_method_for_model : 
            Тест для строкового представления объекта модели Post
    3) test_get_absolute_url : 
            Тест для метода модели get_absolute_url

    4) test_post_creation_object :
            Тест для проверки правильного заполенения атрибутов объекта класса Post
    5) test_homepage_list_view :
           Проверяет доступность домашней страницы по пути "/" , а также по нику "home"
           Проверяет, что на странице присутствует как минимум 1 пост.
    6) test_detail_post_view :
        Проверяет, что post/1 существует
        Проверяет, что других постов нет, например post/20 не существует
        Проверяет , что контент страницы содержит наш пост
        Проверяет, что отображается правильный шаблон

    7) test_update_post_view:
        Проверяет, что при обновлении поста происходит редирект на другую страницу

    8) test_delete_post_view:
        Проверка удаления

    9) test_create_post_view:
        Проверяет, что созданный объект корректен и корректно отображается
        
    """
    def setUp(self):
        # 1 Определяем пользователя и добавляем его в тестовую БД
        self.current_user = get_user_model().objects.create_user(
            username = 'test',
            email = 'test@test.com',
            password = 'secretpassword9000',
        )

        # 2. Определим пост, созданный тестовым пользователем
        self.current_post = Post.objects.create(
            title = 'Test title',
            content = 'Test content',
            author = self.current_user,
        )

    def test_str_method_for_model(self):
        """
        Тест для строкового представления объекта модели Post
        """ 
        post = Post(title='Test title')
        self.assertEqual(str(post), 'Title: Test title')

    def test_get_absolute_url(self):
        """
        Тест для метода модели get_absolute_url
        """
        self.assertEqual(self.current_post.get_absolute_url(), "/post/1/")

    def test_post_creation_object(self):
        """
        Тест для проверки правильного заполенения атрибутов объекта класса Post
        """
        self.assertEqual(str(self.current_post.title), 'Test title')
        self.assertEqual(str(self.current_post.content), 'Test content')
        self.assertEqual(str(self.current_post.author), 'test')

    def test_homepage_list_view(self):
        """
        Проверяет доступность домашней страницы по пути "/" , а также по нику "home"
        Проверяет, что на странице присутствует как минимум 1 пост.
        """
        response_abs = self.client.get("/")
        self.assertEqual(response_abs.status_code, 200)

        response_name = self.client.get(reverse("home"))
        self.assertEqual(response_name.status_code, 200)

        # Блок првоерки содержимого
        self.assertContains(response_name, 'Test content')
        self.assertTemplateUsed(response_name, "home.html")

    def test_detail_post_view(self):
        """
        Проверяет, что post/1 существует
        Проверяет, что других постов нет, например post/20 не существует
        Проверяет , что контент страницы содержит наш пост
        Проверяет, что отображается правильный шаблон
        """
        response_abs = self.client.get("/post/1/")
        self.assertEqual(response_abs.status_code, 200)

        response_name = self.client.get(reverse("detail_post", args=[str(1)]))
        self.assertEqual(response_name.status_code, 200)

        no_response = self.client.get("/post/20/")
        self.assertNotEqual(no_response.status_code, 200)

        self.assertContains(response_name, 'Test content')
        self.assertTemplateUsed(response_name, "detail_post.html")

    def test_update_post_view(self):
        """
        Проверяет, что при обновлении поста происходит редирект на другую страницу
        """ 
        response = self.client.post(reverse("update_post", args=[str(1)]), { 
            'title' : 'Test title updated',
            'content' : 'Test content updated',
        })
        self.assertEqual(response.status_code, 302)

    def test_delete_post_view(self):
        """
        Проверка удаления
        """ 
        response = self.client.get(
            reverse("delete_post", args=[str(1)])
        )
        self.assertEqual(response.status_code, 200)

    def test_create_post_view(self):
        """
        Проверяет, что созданный объект корректен и корректно отображается
        """
        response = self.client.post(
            reverse('create_post') ,
            {
                'title' : 'New test title',
                'content' : 'New test content',
                'author' : self.current_user,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New test title')
        self.assertContains(response,'New test content')