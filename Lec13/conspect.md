## Лекция 13. Стилизация и Bootstrap

***Задача:*** применить стандартную стилизацию при помощи ```css```-фреймворка ```Bootstrap```.
```Bootstrap``` - это ***АДАПТИВНЫЙ*** ```CSS``` кроссплатформенный фреймворк.

### Шаг 1. Реконфигурация существующего проекта.
Возьмем за основу, проект и проложение, созданные в ```Lec12```. В той лекции мы поленились и внутри приложения ```users``` зачем-то оставили домашнюю страницу. Исправим это недоразумение. Создадим новое приложение ```pages``` : ```python manage.py startapp pages``` (сразу зарегестрируем его в ```settings.py```).

После этого в ```project/urls.py``` передадим управление при переходе на домашнюю страницу приложению ```pages```:
```
from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", include("users.urls")), # для передачи управления SignUp
    path("users/", include("django.contrib.auth.urls")), # Для реализации login/logout/passwordchange/passwordreset
    path("", include("pages.urls")) # HomePage будет работать в связке с приложением pages
]

```

Теперь внутри ```pages/urls.py``` создадим связь ```url-view```:
```
from django.urls import path 
from .views import HomePageView 

urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
]
```
***Не забыть убрать эту связь из приложения users!***

Реализуем отображение ```pages/views.py```:
```
from django.views.generic import TemplateView

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html' 

```
***Не забыть убрать эту часть из users/views.py***

### Шаг 2. Перенос стилизации фреймворка Bootstrap
* Заходим на страницу https://getbootstrap.com/
* Вкладка ```Examples```
* Выбираем https://getbootstrap.com/docs/4.5/examples/starter-template/
* Правая кнопка - код страницы - ```copy```
* После чего вставляем в шаблон ```base.html``` и подменяем функционал кнопок и изменяем текст
В итоге, базовый шаблон теперь выглядит так:
```
<!-- templates/base.html -->
<!doctype html>
<html lang="en">
<head>
<!-- Required meta tags -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,
initial-scale=1, shrink-to-fit=no">
<!-- Bootstrap CSS -->
<link rel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/\
bootstrap.min.css"
integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81i\
uXoPkFOJwJ8ERdknLPMO"
crossorigin="anonymous">
<title>{% block title %}Django Blog App{% endblock title %}</title>
</head>
<body>
<nav class="navbar navbar-expand-md navbar-dark bg-dark mb-4">
  <a class="navbar-brand" href="{% url 'home' %}">Django Blog App</a>
    {% if user.is_authenticated %}
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <a href=""> <!--Здесь добавим ссылку на создание поста-->
            + New
          </a>
        </li>
      </ul>
    {% endif %}
<button class="navbar-toggler" type="button" data-toggle="collapse"
data-target="#navbarCollapse" aria-controls="navbarCollapse"
aria-expanded="false" aria-label="Toggle navigation">
<span class="navbar-toggler-icon"></span>
</button>
<div class="collapse navbar-collapse" id="navbarCollapse">
{% if user.is_authenticated %}
<ul class="navbar-nav ml-auto">
<li class="nav-item">
<a class="nav-link dropdown-toggle" href="#" id="userMenu"
data-toggle="dropdown" aria-haspopup="true"
aria-expanded="false">
{{ user.username }}
</a>
<div class="dropdown-menu dropdown-menu-right"
aria-labelledby="userMenu">
<a class="dropdown-item" href="{% url 'password_change' %}">Change password</a>
<div class="dropdown-divider"></div>
<a class="dropdown-item" href="{% url 'logout' %}">Log Out</a>
<div class="dropdown-divider"></div>
<a class="dropdown-item" href="{% url 'password_reset' %}">Password Reset</a>
</div>
</li>
</ul>
{% else %}
<form class="form-inline ml-auto">
<a href="{% url 'login' %}" class="btn btn-outline-secondary">
Log In</a>
<a href="{% url 'signup' %}" class="btn btn-primary ml-2">
Sign up</a>
</form>
{% endif %}
</div>
</nav>
<div class="container">
{% block content %}
{% endblock content %}
</div>
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4\
YfRvH+8abtTE1Pi6jizo"
crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/\
1.14.3/
umd/popper.min.js"
integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbB\
JiSnjAK/
l8WvCWPIPm49"
crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/\
js/bootstrap.min.js"
integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ\
6OW/JmZQ5stwEULTy"
crossorigin="anonymous"></script>
</body>
</html>
```


### Шаг 2.1 Стилизация кнопок
Сейчас у нас перенесен стиль только для шапки и шрифтов. Но кнопки на страницах ```Login``` ```SignUp``` очень страшные.
Исправим эту ситуацию.
* Заходим в ```templates/registration/login.html``` и в коде кнопки пропишем:
```
<button class="btn btn-success ml-2" type=...
```
Аналогично поступим с ```signup.html```.

### Шаг 3. Стилизация веб-форм
Для того, чтобы стилизовать формы на странице необходим адаптер, который будет конвертировать стандартное отображение веб-формы в отображение ```Bootstrap-WebForm```.
* Для получения этого адаптера необходимо выполнить ```pipenv install django-crispy-forms```
* Теперь необходимо сообщить проекту, что вы собираетесь использовать этот адаптер для отображения форм (```3RD party software```)
* Заходим в ```settings.py``` -> ```ISTALLED_APPS``` -> ```crispy_forms```
* В самом низу также добавим ```CRISPY_TEMPLATE_PACK = 'bootstrap4'``` какую версию наборов стилей будем использовать.
* Теперь сообщим всем шаблонам, что они будут использовать ассеты из ```crispy_form```.
* ```templates/signup.html```:
```
<!--templates/signup.html-->
{% extends 'base.html' %}

{% load crispy_forms_tags %} <!--Сообщаем, что будем использовать необходимые crispy ассеты-->

{% block content %}
    <h2>Sign Up Page</h2>
    <form method="post">
        {% csrf_token %}
        {{ form|crispy }} <!--Теперь отображаем форму как указано в crispy-->
        <button class="btn btn-success ml-2" type="submit">Sign Up</button>
    </form>
{% endblock content %}
```
* Тоже самое сделаем внутри ```teplates/registration/login.html```
```
<!--templates/registration/login.html-->
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
    <h2>Login Page</h2>
    <form method="post">
        {% csrf_token %}
        {{ form|crispy }}
        <button class="btn btn-success ml-2" type="submit">Login</button>
    </form>
{% endblock content %}
```

### Шаг 4. Механизмы сброса пароля. Начало.
Стандартный механизм сброса пароля уже реализован в приложении ```django.contrib.auth```. Но нас не устраивают стандартные шаблоны отображений.
Перепишем эти шаблоны. Сейчас создадим набор шаблонов:
```
templates/registration/password_change_form.html
templates/registration/password_change_done.html
```

```
<!--templates/registration/password_change_done.html-->
{% extends 'base.html' %}
```

```
<!--templates/registration/password_change_form-->
{% extends 'base.html' %}
```