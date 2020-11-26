## Лекция 7. Продолжение Лекции 6.

Продолжаем с момента, где остановились в лекции 6.

### Шаг 1. Создадим шаблоны

* Создаем директорию ```templates```
* Сообщаем проекту, откуда тянуть шаблоны ```settings.py``` - > ```TEMPLATES[DIRS]``` : 
```
# settings.py
'DIRS': [os.path.join(BASE_DIR, 'templates')], 
```
* Создадим шаблон ```templates/home.html``` пока оставим пустым

* На уровне ```views.py``` создаем списочное отображение модели (```ListView```):
```
#posts/views.py
from django.views.generic import ListView 

from .models import Post 

# Create your views here.
class HomePageView(ListView):
    # какие объекты мы хотим отображать списком
    model = Post
    template_name = 'home.html'
    # Имя, под которым в шаблоне будут доступны списки постов
    context_object_name = 'posts'
```

* В шаблоне ```templates/home.html``` пропишем логику отображения постов:
```
<!--templates/home.html-->
<h1>Posts List HomePage</h1>
<ul>
    {% for post in posts %}
        <li>{{post}}</li>
    {% endfor %}
</ul>
```
Где ```posts``` - это имя, по которому мы получим список объектов из ```HomePageView``` (см ```context_object_name```).

### Шаг 2. Стандртно создадим свяжем отображение с сылками

* Внутри ```posts/urls.py``` привяжем ```HomePageView``` к пустому url.
```
# posts/urls.py
from django.urls import path 

from .views import HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
]
```
* В проекте ```project/urls.py``` передадим управление нашему приложению ```posts```:
```
# project/urls.py
from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("posts.urls")),
]

```

### Основная идея
Теперь мы можем добавлять новые объекты модели (создавать новые сущности ```Post```) при условии того, что код шаблон никак не будет меняться.
Такие шаблоны (отображать переменное количество элементов, изменяться в ходе функционирования прилоежния) - ***динамические шаблоны***.



### Шаг 4. Тесты
Подумаем о будущем, и создадим тестовый модуль для приложения, который будет проверять правильность работы всей логики.
Для этого выполним тест на 2 пути:
* 1-ый путь : ***Проверка того, что МОДЕЛЬ корректно функционирует***
* 2-ой путь: ***Доступность url + отображается правильный шаблон***

#### 1. Тест модели
Для тестирования модели воспользуемся промежуточной тестовой базой, для этого:
```
# posts/tests.py
from django.test import TestCase
from .models import Post 
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
```
#### 2. Тесты urls + верный шаблон
Для этого напишем 3 теста:
* Проверка доступности по url ```"/"```
* Проверка валидного шаблона (значит что при вызове ```"/"``` показывается шаблон ```home.html```)
* Проверка валидного никнейма для URL (значит, что ВНУТРИ приложения по имени ```home``` идет обращение к адресу ```"/"```)
```
# posts/tests.py
...
from django.urls import reverse
...
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
```
