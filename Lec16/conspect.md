## Разграничение прав доступа и модель Comment

***Проблема***: любой пользователь (аутентифицированный) может изменять/удалять посты чужих пользователей.

***Задача***: разграничить права доступа пользователя на сайте таким образом, что удалять и редактировать можно было только свои посты.

***Решение***: воспользуемся стандартным классом ```PermissionDenied```.

### Шаг 1. Усовершенствование Update и Delete отображений
Поскольку для реализации функционала задействованы отображения ```PostEditView``` и ```PostDeleteView``` их необходимо переработать.
Любой базовый шаблон для ```view``` имеет под капотом метод ```dispatch()```. Переходим к редактированию этих отображений:
```
...
from django.core.exceptions import PermissionDenied
...

class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post 
    template_name = "edit_post.html"
    fields = ("title", "body")
    context_object_name = "post"
    login_url = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        """
        /posts/1/edit/ при переходе , например, по данной ссылке отрабатывает следующая последовательность действий:
        * вызывается отображение PostEditView.as_view()
        * затем вызывает метод dispatch()
        * если dispatch() не провоцирует исключений - получаем доступ к запросу, показываем шаблон, заполняем форму
        * если dispatch() кидает исключение - валимся с 403 ошибкой
        """
        post_object = self.get_object() # Post на странице
        if post_object.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "delete_post.html"
    success_url = reverse_lazy("list_posts")
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        """
        /posts/1/delete/ при переходе , например, по данной ссылке отрабатывает следующая последовательность действий:
        * вызывается отображение PostDeleteView.as_view()
        * затем вызывает метод dispatch()
        * если dispatch() не провоцирует исключений - получаем доступ к запросу, показываем шаблон, заполняем форму
        * если dispatch() кидает исключение - валимся с 403 ошибкой
        """
        post_object = self.get_object() # Post на странице
        if post_object.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

```


### Шаг 2. Добавление модели комментариев.
Реализуем модель ```Comment``` в файле ```posts/models.py```
```
class Comment(models.Model):
    comment = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE) 
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.comment 

    def get_absolute_url(self):
        return reverse("list_posts") 
```

Связь (реляция) ```Many-to-One``` трактуется из следующих соображений:
* У коммента есть автор. Единовременно у коммента не больше 1-го автора. Но у автора может быть ***гораздо больше*** комментов.
* Коммент привязан к посту. Единовременно комментарий привязывается только к 1 посту. Но у поста может быть ***гораздо больше*** комментов.

### Шаг 3. Подготовка запросов для миграции
* Генерация миграционных запросов осуществляется при поищи : ```python manage.py makemigrations posts```
* Применение сгенерированных запросов: ```python manage.py migrate```

### Шаг 4. Конфигурация панели администратора
Самый простой выбор - зарегестрируем модель в интерфейсе админа.
Теперь изменим классическое отображение на ```StackedModel``` или ```TabularInline```.
```
from django.contrib import admin
from .models import Post , Comment

class CommentInline(admin.TabularInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline
    ]

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
```

### Шаг 5. Указание явного типа реляций
Для того, чтобы из объекта ```Post``` можно было дотянться до соответствующего ему комментарию, в модели ```Comment``` внесем изменения в поле: 
```
...
post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') 
...
```
Теперь при вызове ```Post.comments``` получим доступ к ассоциированным с этим объектом комментариям. Теперь обновим миграции:
* Генерация миграционных запросов осуществляется при поищи : ```python manage.py makemigrations posts```
* Применение сгенерированных запросов: ```python manage.py migrate```
* Запусти сервер : ```python manage.py runserver```


### Шаг 6. Редактирование шаблонов для отображения постов
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
            <a href="{% url 'edit_post' post.pk %}">Edit</a> | <a href="{% url 'delete_post' post.pk %}">Delete</a>
        </div>
        <div class="card-footer text-center text-muted">
            {% for comment in post.comments.all %}
            <p>
                <span class="font-weight-bold">{{comment.author }}</span> says : {{comment}}
            </p>
            {% endfor %}
        </div>
    </div>
    <br/>
    {% endfor %}
{% endblock content %}
```

### Шаг 7. В качестве практикума
Добавить формы для добавления комментария сразу под постом (без выхода в панель администратора) ***НЕОБЯЗАТЕЛЬНО***.