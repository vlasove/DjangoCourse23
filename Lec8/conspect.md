## Лекция 8. Добавим CSS + сделаем индивидуальные страницы для каждого поста
Для начала проведем стандартную подготовку:
* ```pipenv shell```
* ```pipenv install django```
* ```django-admin startproject project .```
* ```python manage.py startapp simpleblog```

* Не забудем зарегестрировать приложение для проекта ```settings.py-> INSTALLED_APPS ...```
* Применим стандартные миграции ```python manage.py migrate```
* Проверим что все запускается ```python manage.py runserver```
* ***ОК!***

### Шаг 1. Создаем модель поста
Возьмем за образец стандартную структуру поста:
* ```title``` - название поста
* ```content``` - тел поста
* ```author``` - автор поста (стандартная модель пользователя Django, тип реляции ```ONE -TO - MANY```)
Для ее создания заходим в ```models.py```:


```
from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    # В поле автора мы помещаем реляцию со стандартной пользовательской моделью Django
    # auth.User - стандартный юзер в Django
    # Создаем соотношение ONE-TO-MANY (по отношению к автору)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return "Title: " + self.title
```

### Шаг 2. Настройка админа
Для корректной работы из-под панели администратора необходимо:
* Создать ```superuser```: ```python manage.py createsuperuser```
* Зарегестрировать нашу модель в интерфейса админа ```simpleblog/admin.py```
```
#simpleblog/admin.py
from django.contrib import admin
from .models import Post 

# Register your models here.

admin.site.register(Post)
```
* Зайдем в админа и создадим 3 поста.

### Шаг 3. Конфигурируем связь проект-приложение
* 1. В ```project/urls.py``` добавим :
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("simpleblog.urls")),

]
```
* 2. В ```simpleblog/urls.py``` добавим:
```
from django.urls import path 

from .views import PostListView

urlpatterns = [
    path("", PostListView.as_view(), name="home"),
]
```
* 3. Теперь создадим ```PostListView``` в ```simpleblog/views.py```:
```
from django.views.generic import ListView
from .models import Post
# Create your views here.

class PostListView(ListView):
    """
    Класс для отображения набора постов. Набор постов адресуется шаблону home.html
    Внутри шаблона набор постов доступен по имени `posts`
    """
    model = Post 
    template_name = "home.html"
    context_object_name = "posts"
```

### Шаг 4. Работа с шаблоном
* Создадим директорию ```templates``` и 2 файла ```templates/base.html```, ```templates/home.html```
* Подскажем где лежат шаблоны ```settings.py``` -> ```TEMPLATES[DIRS]``` - > ```'DIRS': [os.path.join(BASE_DIR, 'templates')],```

* Опишем шаблон ```base.html```:
```
<!--templates/base.html-->
<html>
    <head>
        <title>My MicroBlog app</title>
    </head>
    <body>
        <header>
            <h1>
                <a href="{% url 'home' %}">Home to Blog</a>
            </h1>
        </header>
        <div>
            {% block content %}
            {% endblock content %}
        </div>
    </body>
</html>
```
* Опишем шаблон ```home.html```:
```
<!--templates/home.html-->
{% extends 'base.html'%}

{% block content %}
    {% for post in posts %}
        <div class="post-entry">
            <h2>
                <a href="">{{post.title}}</a>
            </h2>
            <p>
                {{post.content}}
            </p>
            <p>
                By : {{post.author}}
            </p>
        </div>
    {% endfor%}
{% endblock content %}
```

* Запустим проект ```python manage.py runserver```

### Шаг 5. Делаем стильно
Чтобы сделать стильно, нам нужен ```CSS```.
* Для этого создадим директорию с названием ```static``` (в корне проекта)
* Подскажем где искать ```static``` -> ```settings.py``` -> в самом низу файла добавим:
```
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```
* Внутри директории ```static``` создадим файл ```static/css/base.css```
```
/* comment static/css/base.css */
header h1 a {
    color : rebeccapurple;
}
```
* Вкрути ***СТИЛЬ*** в базовый шаблон
```
<!--templates/base.html-->
{% load static %}
<html>
    <head>
        <title>My MicroBlog app</title>
        <link href="{% static 'css/base.css' %}" rel="stylesheet">
    </head>
    <body>
......
```

### Шаг 6. Это стильно, но пока бесполезно.
Создадим индивидуальные страницы для каждого поста.
Для этого:
* Создадим отображение индивидуального поста (```DetailView``` - отображение одного элемента ```ListView```):
```
#simpleblog/views.py
from django.views.generic import ListView, DetailView
...
class PostDetailView(DetailView):
    """
    Класс для детального отображения поста. Пост адресуется шаблону detail_post.html
    Внутри шаблона пост доступен по имени `post`
    """
    model = Post 
    template_name = "detail_post.html"
    context_object_name = "post"

```
* Создадим шаблон ```detail_post.html```
```
<!--templates/detail_post.html-->
{% extends 'base.html' %}

{% block content %}
    <div class="post-entry">
        <h2>
            {{post.title}}
        </h2>
        <h3>
            By : {{post.author}}
        </h3>
        <p>
            {{post.content}}
        </p>
    </div>
{% endblock content %}
```

* Создадим динамический URL-компонент ```simpleblog/urls.py```:
```
urlpatterns = [
    path("post/<int:pk>", PostDetailView.as_view(), name="detail_post"), #dynamic URL link
    path("", PostListView.as_view(), name="home"),
]

```
* Изменим ```home.html```:
```
<!--templates/home.html-->
{% extends 'base.html'%}

{% block content %}
    {% for post in posts %}
        <div class="post-entry">
            <h2>
                <a href="{% url 'detail_post' post.pk %}">{{post.title}}</a>
            </h2>
            <p>
                {{post.content}}
            </p>
            <p>
            ...
```

### Шаг 7. Проверим, что все работает.
```python manage.py runserver```


