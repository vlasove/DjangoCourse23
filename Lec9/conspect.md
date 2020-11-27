## Лекция 9. Веб-формы

Скопируем структуру проекта из ```Lec8``` и продолжим с того места, где остановились в прошлый раз.

***Что хотим?*** : хотим, чтобы процесс создания/удаления/редактирования единиц (постов) можно было осуществлять через интерфейс с веб-страниц, а не через панель администратора, как было в ```Lec8```.

### Шаг 1. Добавим кнопку ```+New Post``` к шаблону.
Изменим шаблон ```templates/base.html``` и добавим в него ссылку для создания нового поста:
```
<!--templates/base.html-->
{% load static %}
<html>
    <head>
        <title>My MicroBlog app</title>
        <link href="{% static 'css/base.css' %}" rel="stylesheet">
    </head>
    <body>
        <header>
            <div class="nav-left">
                <h1>
                    <a href="{% url 'home' %}">Home to Blog</a>
                </h1>
            </div>

            <div class="nav-right">
                <!--Need to add post_creation_view to href-->
                    <a href="{% url 'create_post' %}">+ Create New Post</a>
            </div>
        </header>
            ......
```

### Шаг 2. Создадим правило отображения страницы с созданием нового поста
* Для создания отображения необходимо сначала в ```simpleblog/urls.py``` указать правило переадресации управления нашему отображению:
```
# simpleblog/urls.py

from django.urls import path 

from .views import PostListView, PostDetailView, PostCreateView

urlpatterns = [
    path('post/create/', PostCreateView.as_view(), name = 'create_post'), # Добавляем view для отображения формы создания Поста
    path("post/<int:pk>", PostDetailView.as_view(), name="detail_post"), #post/1 pk == id из модели 
    path("", PostListView.as_view(), name="home"),
]
```

* После чего создадим правило отображения в файле ```views.py```:
```
from django.views.generic import CreateView
.....

class PostCreateView(CreateView):
    """
    Класс для отображения веб-формы создания поста.
    Для корректного оторражения требуется указание модели, шаблона, название отображаемых полей
    """
    model = Post 
    template_name = 'create_post.html'
    fields = '__all__' # Пока отображаем все поля в веб-форме (исключается только id)
```
* Теперь создадим шаблон ```templates/create_post.html```:
```
<!--templates/create_post.html-->
{% extends 'base.html' %}

{% block content %}
    <h1>Веб-форма для создания нового поста</h1>
    <form method="post">
        {% csrf_token %}
        {{form.as_p}}
        <input type="submit" value="Create Post"/>
    </form>
{% endblock content %}
```
***csrf-token*** - способ, обойти проблему множественного (одновременного) запроса от формы к созданию новой строки в БД. Позволяет создать очередь запросов на уровне шаблона, который могут быть без вреда (по-очереди) обработаны моделью (БД).

### Шаг 3. Настраиваем редирект на уровне модели
Из-за того, что после нажатия кнопки ```submit``` у нас отсутствует правило перенаправления пользователя на другие страницы, мы получаем ошибку. Для ее решение можно:
* установить redirect на уровне шаблона/отображения
* установить редирект на уровне модели при помощи метода ```get_absolute_url``` +++

Переходим в модель ```simpleblog/models.py``` и добавляем метод ```get_absolute_url```:
```
from django.db import models
from django.urls import reverse

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
    
    # new part
    def get_absolute_url(self):
        return reverse("detail_post", args=[str(self.id)])# reverse('home') - переадресация на домашнюю страницу
```

Выбирая между редиректом на детальный вид поста или домашнюю страницу - нужно подумать, насколько пользователю будет удобно работать с сервисом.


### Шаг 4. Создадим форму для Редактирования Поста
Теперь создадим блок для обновления информации о посте. 
* Для этого сначала определим url-ссылку по которой будем попадать на страничку с формой обновления поста. Заходим в ```simpleblog/urls.py```:
```
from django.urls import path 

from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView

urlpatterns = [
    path("post/<int:pk>/update", PostUpdateView.as_view(), name = 'update_post'), # view для отображения формы update
    path('post/create/', PostCreateView.as_view(), name = 'create_post'), # Добавляем view для отображения формы создания Поста
    path("post/<int:pk>", PostDetailView.as_view(), name="detail_post"), #post/1 pk == id из модели 
    path("", PostListView.as_view(), name="home"),
]
```

* Затем в файле ```simpleblog/views.py``` создадим ```PostUpdateView```:
```
class PostUpdateView(UpdateView):
    """
    Класс для отображения веб-формы обновления поста.
    Для корректного отображения требуется указание модели, шаблона, название отображаемых полей
    """
    model = Post 
    template_name = 'update_post.html'
    fields = ["title", "content"] # Не хотим , чтобы юзер мог поменять автора поста, а title и content - ок!
```

* Создадим шаблон ```templates/update_post.html```:
```
<!--templates/update_post.html-->
{% extends 'base.html' %}

{% block content %}
    <h1>Веб-форма для обновления поста</h1>
    <form method="post" action="">
        {% csrf_token %}
        {{form.as_p}}
        <input type= "submit" value="Update Post"/>
    </form>
{% endblock content%}
```

* Теперь на ```detail_post.html``` добавим кнопку, которая будет переадресовывать на страничку с обновлением содержания поста:
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
    <!--Это добавление кнопки с перенаправлением на страничку обновления содержимого-->
    <a href="{% url 'update_post' post.pk %}">+ Update</a>
{% endblock content %}
```

### Шаг 5. Создадим форму для Удаления Поста
* В шаблоне ```templates/detail_post.html``` добавим кнопку с переадресацией на удаление.
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
    <!--Это добавление кнопки с перенаправлением на страничку обновления содержимого-->
    <p>
        <a href="{% url 'update_post' post.pk %}">+ Update</a>
    </p>
    <p>
        <a href="{% url 'delete_post' post.pk %}">- Delete</a>
    </p>
    
{% endblock content %}
```

* Создадим шаблон для удаления поста ```templates/delete_post.html```:
```
<!--templates/delete_post.html-->
{% extends 'base.html' %}

{% block content %}
    <h1>Форма для удаления поста</h1>
    <form method="post" action ="">
        {% csrf_token %}
        <p>
            Вы уверены, что хотите удалить этот пост?
        </p>
        <input type="submit" value="Delete Post"/>
    </form>
{% endblock content %}
```

* Создадим отображение ```PostDeleteView``` в файле ```simpleblog/views.py```:
```
from django.urls import reverse_lazy

class PostDeleteView(DeleteView):
    """
    Класс для отображения веб-формы удаления поста.
    Для корректного отображения требуется указание модели, шаблона, КУДА перенаправлять после удаления
    """
    model = Post 
    template_name = 'delete_post.html'
    success_url = reverse_lazy("home") # Редирект выполняется ПОСЛЕ нажатия на кнопку `submit`. Обычный reverse() выполнился бы ДО.
```

* Добавим вызов отображения в ```simpleblog/urls.py```:
```
from django.urls import path 

from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="delete_post"),  # форма для удаления поста
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name = 'update_post'), # view для отображения формы update


    path('post/create/', PostCreateView.as_view(), name = 'create_post'), # Добавляем view для отображения формы создания Поста
    path("post/<int:pk>/", PostDetailView.as_view(), name="detail_post"), #post/1 pk == id из модели 
    path("", PostListView.as_view(), name="home"),
]
```