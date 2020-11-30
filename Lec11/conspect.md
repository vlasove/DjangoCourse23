## Лекция 11. Accounting

***Задача:*** добавить в проект пользователя. Необходимо реализовать механизмы:
* ```Log In``` (аутентификация)
* ```Log Out```
* ```Sign Up``` (регистрация => авторизация)

***Аутентификация*** - это процесс узнавания (свой-чужой).
***Авторизация*** - это процесс выдачи прав доступа.

Для того, чтобы реализовать выше перечисленные механизмы нам подобится какой-то ```User``` объект.

Предлагается следующее: чтобы не писать пользователя с нуля, воспользуемся стандартным пользователем Django ```auth.User```.
В ```auth.User``` по умолчанию реализовано достаточно много полезного функционала. 
```
# если открыть документацию /исходники
class User(........):
    self.username = ....
    self.password = ....
    self.email = ....
    self.first_name = ....
    self.last_name = ....

    ....
    self.is_authenticated = [true, false]
```

### Шаг 1. Реализуем механизм Log In
В Django есть стандартный механизм для реализации процесса ```Log In```. Для начала необходимо передать управление в проекте приложению 
```django.contrib.auth.urls``` (стандартное приложение, предустановленное).
```
#simpleblog/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # по пути 'accounts/' передадим управление приложению auth
    path("", include("simpleblog.urls")),

]
```

### Шаг 2. Реализуем связь с стандартным приложением ```auth```
```LoginView``` нам реализовывать не нужно, тк данное отображение является частью приложения ```auth```. Единственное, что необходимо сделать,
это создать шаблон по адресу ```registration/login.html```.
Внутри ```auth``` существует свой ```LoginView``` и его реализация такова, что :
```
class LoginView(....):
    ......
    template_name = 'registration/login.html'
    ......
``` 
***Создадим*** файл по адресу ```registration/login.html``` для связи со стандартным ```LoginView```.
```
<!--templates/registration/login.html-->
{% extends 'base.html' %}


{% block content %}
    <h2>Страница Log In</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type "submit">Log In</button>
    </form>
{% endblock content %}
```
***Необходимо*** подсказать проекту, куда перенаправлять пользователя после того, как он пройдет ```Log In``` (пройдет аутентификацию).
Для этого в файле ```project/settings.py``` -> в самый низ -> ```LOGIN_REDIRECT_URL = 'home'```.

После убедимся что все работает, для этого ```python manage.py runserver``` -> ```accounts/login/```.

### Шаг 3. Переделаем шаблон, чтобы отображать для верификации Log In
Сделаем визуальное отображение, для того , чтобы знать - залогинин (аутентифицирован ли) текущий пользователь или нет.
Для этого воспользуемся полем ```auth.User.is_authenticated```.
Заходим в ```templates/base.html```:
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
        
        {% if user.is_authenticated %}
        <!-- Если пользователь залогинен, будем писать "Current user: username"-->
            <p>Current user {{user.username}}</p>
        {% else %}
        <!-- Если пользователь не залогинен будем писать "You are not logged. Log In"-->
            <p>
                You are not logged. <a href="{% url 'login' %}">Log In Now</a>
            </p>
        {% endif %}


        <div>
            {% block content %}
            {% endblock content %}
        </div>
    </body>
</html>
```

Снова проверим, что все работает ```python manage.py runserver```.

### Шаг 4. Реализация механизма Log Out
Стандартный механизм ```Log Out``` реализован также внутри приложения ```django.contrib.auth```. Для того, чтобы им воспользоваться, необходимо перейти по никнейм-ссылке ```logout```. Реализовывать шаблоны не нужно. Соответственно, встроим в шаблон ```templates/base.html``` кнопку ```logout```.
```
....
        {% if user.is_authenticated %}
        <!-- Если пользователь залогинен, будем писать "Current user: username"-->
            <p>Current user {{user.username}}</p>
            <p>
                <a href="{% url 'logout' %}">Log Out</a>
            </p>
        {% else %}
        <!-- Если пользователь не залогинен будем писать "You are not logged. Log In"-->
            <p>
                You are not logged. <a href="{% url 'login' %}">Log In Now</a>
            </p>
        {% endif %}
...
```
Теперь осталось подсказать Django куда перенаправлять, после успешного выполнения ```LogOut```. Для этого заходим в ```settings.py``` -> в самый низ -> ```LOGOUT_REDIRECT_URL = 'home' ```.

### Пара слов о том, как работает аутентификация.
При выполненнии ```Log In``` пользователь предоставляет о себе информацию в виде ```username``` и ```password```. После этого Django пытается найти в базе данных пользователей, кого-нибудь c таким же ```username```. (Если уже тут не находите таког опользователя, то аутентификация не может быть завершена - попросту некого аутентифицировать - вы не знаете об этом пользователе ничего.)
В случае, если кто-то с именем ```username``` присутсвует в базе, то из базы выбирается его пароль ```password_from_db``` и сопоставляете его с ```password``` который принес пользователь через форму ```LogIn``` на сайте. В случае, если пароли совпадают - то аутентификация считается успешной и происходит редирект на ```home```, в противном случае - аутентификация успешно не выполняется.


### Шаг 5. Созданием механизма SignUp
Стандартной процедуры для регистрации не существует. Для этого нам придется ее реализовать самостоятельно.

* Создадим новое приложение ```python manage.py startapp accounts```
* Зарегестрируем приложение в проекте ```settings.py``` -> ```INSTALLED_APPS``` -> ```accounts.apps.AccountsConfig```.
* После этого в проекте ```simpleblog/urls.py```:
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # по пути 'accounts/' передадим управление приложению auth
    path('accounts/', include('accounts.urls')), # Это передача управления приложению с реализацией SignUp
    path("", include("simpleblog.urls")),

]
```

* В приложении ```accounts/urls.py```:
```
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
]
```

* В отображениях ```accounts/views.py```:
```
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login') 

```
* В ```templates/signup.html```:
```
<!--templates/signup.html-->
{% extends 'base.html' %}

{% block content %}
    <h2>Страница авторизации</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Authorize/SignUp</button>
    </form>
{% endblock content%}
```
* Теперь отобразим кнопку ```SignUp``` в ```templates/base.html```:
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

        {% if user.is_authenticated %}
        <!-- Если пользователь залогинен, будем писать "Current user: username"-->
            <p>Current user {{user.username}}</p>
            <p>
                <a href="{% url 'logout' %}">Log Out</a>
            </p>
        {% else %}
        <!-- Если пользователь не залогинен будем писать "You are not logged. Log In"-->
            <p>
                You are not logged. <a href="{% url 'login' %}">+ Log In Now</a> or <a href = "{% url 'signup'%}"> + Sign Up Now</a>
            </p>
        {% endif %}


        <div>
            {% block content %}
            {% endblock content %}
        </div>
    </body>
</html>
```