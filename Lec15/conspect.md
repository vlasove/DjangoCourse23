## Лекция 15. Собираем первую версию блога

***Задача*** : на данный момент в нашем проекте ест ьвсе необходимое для работы с аккаунтами , а также ест ьприложение , отвечающее за показ служебных веб страниц (```pages```). Теперь реализуем необходимое приложение для работы полноценного блока - ```posts```.
Создаем приложение ```posts``` : ```python manage.py startapp posts```.

### Шаг 1. Регистрируем приложение
```settings.py``` -> ```ISTALLED_APPS``` -> 'posts.apps.PostsConfig```
А также укажем проекту, какую TimeZone использовать :
```settings.py``` -> ```TIME_ZONE``` -> ```TIME_ZONE = "Europe/Moscow"```

### Шаг 2. Создаем модель Post
В файле ```posts/models.py``` опишем модель ```Post```:
```
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


    def __str__(self):
        return self.title 


    def get_absolute_url(self):
        return reverse("detail_post", args=[str(self.id)])
```

Подготовка и выполнение миграции:
```
python manage.py makemigrations posts
python manage.py migrate
```

***Регистрация*** в панели администратора. ```posts/admin.py``` ->
```
from django.contrib import admin
from .models import Post 

# Register your models here.
admin.site.register(Post)

```

Проверим , что все работает : ```python manage.py runserver``` -> ```admin``` -> создать 2-3 поста.

### Шаг 3. Описание логики приложения
Теперь необходимо определить все ```urls```, ```views``` и ```templates``` для работы данного приложения.

### Шаг 3.1. Перенаправление работы на приложение posts
```project/urls.py```
```
from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", include("users.urls")), # для передачи управления SignUp
    path("users/", include("django.contrib.auth.urls")), # Для реализации login/logout/passwordchange/passwordreset
    path("posts/", include("posts.urls")), # Передача управления приложению Posts
    path("", include("pages.urls")) # HomePage будет работать в связке с приложением pages
]

```

### Шаг 3.2. Описание логики urls уровня приложения
```posts/urls.py``` ->
```
from django.urls import path 
from .views import PostsListView , PostEditView, PostDetailView, PostDeleteView

urlpatterns = [
    path("", PostsListView.as_view(), name="list_posts"),
    path("new/", PostCreateView.as_view(), name="new_post"),
    path("<int:pk>/edit/", PostEditView.as_view(), name="edit_post"),
    path("<int:pk>/", PostDetailView.as_view(), name="detail_post"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="delete_post")
]
```

### Шаг 3.3. Описание необходимых views уровня приложения
```posts/views.py``` ->
```
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from .models import Post

class PostCreateView(CreateView):
    model = Post 
    template_name = "new_post.html"
    fields = ("title", "body", "author")


#   PostDeleteView
# Create your views here.
class PostsListView(ListView):
    model = Post 
    template_name = "list_posts.html"
    context_object_name = "posts"

class PostDetailView(DetailView):
    model = Post 
    template_name = "detail_post.html"
    context_object_name = "post"

class PostEditView(UpdateView):
    model = Post 
    template_name = "edit_post.html"
    fields = ("title", "body")
    context_object_name = "post"

class PostDeleteView(DeleteView):
    model = Post
    template_name = "delete_post.html"
    success_url = reverse_lazy("list_posts")


```

### Шаг 3.4 Создание шаблонов
```templates/list_posts.html```
```
<!--templates/list_posts.html-->
{% extends 'base.html' %}

{% block content %}
    {% for post in posts %}
    <div class="card">
        <div class="card-header">
            <span class="font-weight-bold">{{post.title}}</span>
            <span class="text-muted">by {{post.author}} |
            {{post.date}} </span>
        </div>
        <div class="card-body">
            {{ post.body }}
        </div>
        <div class="card-footer text-center text-muted">
            <a href="#">Edit</a> | <a href="#">Delete</a>
        </div>
    </div>
    <br/>
    {% endfor %}
{% endblock content %}
```
```templates/detail_post.html```
```
<!--templates/detail_post.html-->
{% extends 'base.html' %}

{% block content %}
    <div class="article-entry">
        <h2>{{post.title}}</h2>
        <p>by {{post.author}} | {{post.date}}</p>
        <p>{{post.body}}</p>
    </div>
    <p>
        <a href="{% url 'edit_post' post.pk %}">Edit</a>
        |
        <a href="{% url 'delete_post' post.pk %}">Delete</a>

    </p>
    <p>
        Back to <a href = "{% url 'list_posts'%}"> all posts</a>.
    </p>
{% endblock content%}
```
```templates/edit_post.html```
```
<!--templates/edit_post.html-->
{% extends 'base.html' %}

{% load crispy_forms_tags %}

{% block content %}
    <h1>Edit Post</h1>
    <form method="post" action="">
        {% csrf_token %}
        {{ form|crispy }}
        <button class="btn btn-info ml-2" type="submit">Edit</button>
    </form>"
{% endblock content %}
```
```templates/delete_post.html```
```
<!--templates/delete_post.html-->
{% extends 'base.html' %}

{% block content %}
    <h1>Delete Post</h1>
    <form action="" method="post">
        {% csrf_token %}
        <p>Are you  sure you want to delete this post?</p>
        <button class="btn btn-danger ml-2" type="submit">Delete</button>
    </form>
{% endblock content %}
```

```templates/new_post.html```
```
<!--templates/new_post.html-->
{% extends 'base.html' %}

{% load crispy_forms_tags %}

{% block content %}
    <h1>New Post</h1>
    <form action="" method="post">
        {% csrf_token %}
        {{ form|crispy }}
        <button class="btn btn-success ml-2" type="submit">Create</button>
    </form>
{% endblock content %}
```

## Шаг 3.5. Переверстка домашней страницы
Сделаем супер стильную домашнюю страницу!
```
<!--templates/home.html-->
{% extends 'base.html' %}

{% block content %}
    <div class="jumbotron">
        <h1 class="display-4">Django Portfolio Blog</h1>
        <p class="lead">Simple blog builded with Django</p>
        <p class="lead">
            <a class="btn btn-primary btn-lg" href="{% url 'list_posts' %}" role="button">View All Posts</a>
        </p>
    </div>
    
{% endblock content%}
```


### Шаг 4. Запрет на выбор автора при создании поста
Хотим чтобы автор определялся автоматически при создании поста.
Будем назначать автором поста текущего пользователя.
Переходим на уровень отображения ```posts/views.py```:
```
class PostCreateView(CreateView):
    model = Post 
    template_name = "new_post.html"
    fields = ("title", "body")

    def form_valid(self, form):
        form.instance.author = self.request.user#Singleton pattern
        return super().form_valid(form)
```

### Шаг 5. Запретим создавать посты незалогиненым пользователям

Переходим на уровень отображения ```posts/views.py```:
```
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post

#   PostDeleteView
# Create your views here.
class PostsListView(LoginRequiredMixin, ListView):
    model = Post 
    template_name = "list_posts.html"
    context_object_name = "posts"
    login_url = 'login'

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post 
    template_name = "detail_post.html"
    context_object_name = "post"
    login_url = 'login'

class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post 
    template_name = "edit_post.html"
    fields = ("title", "body")
    context_object_name = "post"
    login_url = 'login'

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "delete_post.html"
    success_url = reverse_lazy("list_posts")
    login_url = 'login'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post 
    template_name = "new_post.html"
    fields = ("title", "body")
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user#Singleton pattern
        return super().form_valid(form)

```

