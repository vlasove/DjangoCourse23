from django.test import TestCase
from .models import Post 
from django.urls import reverse 

"""
Функция reverse(name) возвращает url адрес, сопоставленый никнейму name
"""
# Create your tests here.

class PostModelTest(TestCase):
    """
    Класс для тестирования модели Post
    """
    # Для тестовой БД выполним конфигурацию
    # Все конфигуративы (действия), которые будут выполнены ПЕРЕД КАЖДЫМ ТЕСТОМ
    # помещаем в метод с названием setUp
    def setUp(self):
        """
        Добавим один объект в модель Post
        """
        Post.objects.create(text="Test text for my model")

    def test_text_in_model(self):
        """
        Проверка валидности создания объекта Post с полем text = `Test text for my model`
        """
        current_post = Post.objects.get(id=1)
        expected_text = "Test text for my model"
        self.assertEqual(current_post.text, expected_text)


class HomePageViewTest(TestCase):
    def test_homepage_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_homepage_template(self):
        """
        Проверка на то, что при вызове "/" отображается home.html
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_homepage_by_name(self):
        """
        Проверка на то, что ВНУТРИ приложения по имени "home" отдается именно страница с адресом "/"
        и отображается шаблон home.html
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")