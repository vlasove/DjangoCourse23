### Пару слов про github.com

* Установить git локально 
* Создать guthub репозиторий
* В локальной папке (директории) выполняем ```git init```
* После этого добавляем в индекс все файлы, находящиеся в папке ```git add .```
* Создадим отпечаток в истории проекта ```git commit -m "message to commit"```
* Связываем локальный репозиторий с удаленным ```git remote add origin https://user/.....``` (всего 1 раз, во все остальные разы привязка сохранится)
* Отправим все локальные файлы в удаленный репозиторий ```git push -u origin master```

## Лекция 12. Собственная модель User
***Задача***: создать собственную модель пользователя и прописать всю сопутствующую логику для этого.

### Шаг 1. Конфигурация нового проекта
* Имя проекта ```project```
* Имя приложения ```users```

Пока не выполняем миграции, т.к. может произойти конфликт на уровне таблиц ```User```. В файле ```project/settings.py``` пропишем, что используем собственную модель пользователя:
```
# settings.py
....
# Сообщаем Django что используем своего собственного пользователя
AUTH_USER_MODEL = 'users.MyUser'
```

### Шаг 2. Описание пользовательской модели
Внутри файла ```users/models.py``` необходимо прописать всю логику модели ```MyUser```. Эту модель можно начать строить с самого нуля (это очень долго). Воспользуемся принципом ООП (Наследование) и создадим своего пользователя на основе нискоуровней заглушки в виде ```AbstractUser```. При реализации наследования добавим новое поле - возраст (```age```) в модель.
```
# users/models.py
from django.db import models
# Импортируем абстрактного пользователя
from django.contrib.auth.models import AbstractUser

# Create your models here.
class MyUser(AbstractUser):
    age = models.IntegerField(null=True, blank=True) # null - это означает, что в базе данных, в случае не указания возраста будет стоять NULL
                                                     # blank - допускается создание ОБЪЕКТА MyUser без указания age - информация для валидации форм
                                                     
```

### Шаг 3. Формы-интерфейсы взаимодействия с пользователем
Для того, чтобы создать интерфейс взаимодействия с нашей моделью, необходимо реализовать набор форм (интерфейсов). Создадим файл
```users/forms.py```.
```
# Это именно низкоуровневые интерфейсы взаимодействия с моделью
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import MyUser

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser 
        fields = UserCreationForm.Meta.fields + ('age',)

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = MyUser
        fields = UserChangeForm.Meta.fields # допишу что понадобится
```
Переопределение мета-классов - единственное что нам необходимо поменять при использовании.

После этого создадим интерфейс администратора и свяжем его с нашей моделью через уже готовые интерфейсы взаимодействия (файл ```users/admin.py```):
```
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import MyUserChangeForm, MyUserCreationForm
from .models import MyUser
# Register your models here.

class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser 

admin.site.register(MyUser, MyUserAdmin) # Регистрируем нашу модель для админ-интерфейса, который настроили выше
```

### Шаг 4. Подготовка и накат миграций
* Подготовка миграции (создание запросов к бд) происходит при помощи команды ```python manage.py makemigrations users```
* Применение миграции (применение подготовленных запросов) : ```python manage.py migrate```

### Шаг 5. Суперпользователь
Создадим суперпользователя и попробуем попасть в панель администратора:
* ```python manage.py createsuperuser```
* ```python manage.py runserver``` -> ```admin/```

Пусть в панели админа отображается еще и возраст, для этого в интерфейсе админа ```users/admin.py```:
```
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import MyUserChangeForm, MyUserCreationForm
from .models import MyUser
# Register your models here.

class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser 
    list_display = ["username", "email", "age", "is_staff"]

admin.site.register(MyUser, MyUserAdmin) # Регистрируем нашу модель для админ-интерфейса, который настроили выше
```

### Шаг 6. Аутентификация нашего пользователя
* Создадим директорию ```templates``` и ```templates/registration```
* Теперь сообщим Django где лежат шаблоны ```settings.py``` -> ```TEMPLATES['DIRS']``` :
```
...
'DIRS': [os.path.join(BASE_DIR, 'templates')],
...
```
* В самом низу файла ```settings.py```:
```
# Куда перенаправлять после Log In
LOGIN_REDIRECT_URL = 'home'
# Куда перенаправлять после Log Out
LOGOUT_REDIRECT_URL = 'home'
```
* Создадим файлы:
```
templates/registration/login.html
templates/base.html
templates/home.html
templates/signup.html
```

### Шаг 7. Описываем шаблоны
* ```templates/base.html```
```
<!--templates/base.html-->
<html>
    <head>
        <title>My New App with User</title>
    </head>
    <body>
        {% block content %}
        {% endblock content %}
    </body>
</html>
```
* ```templates/home.html```
```
<!--templates/home.html-->
{% extends 'base.html' %}

{% block content %}
    {% if user.is_authenticated %}
    <p>Привет, {{ user.username}}!</p>
    <p>
        <a href="{% url 'logout' %}"
    </p>
    {% else %}
    <p>
        Ты не залогинен. <a href="{% url 'login' %}">Логин</a>  | <a href="{% url 'signup' %}">Зарегестрироваться</a>
    </p>
    {% endif %}
{% endblock content%}
```

* ```templates/registration/login.html```
```
<!--templates/registration/login.html-->
{% extends 'base.html' %}

{% block content %}
    <h2>Страница для логина</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p}}
        <button type="submit">Логин</button>
    </form>
{% endblock content %}
```

* ```templates/signup.html```
```
<!--templates/ышптгз.html-->
{% extends 'base.html' %}

{% block content %}
    <h2>Страница для регистрации</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p}}
        <button type="submit">Зарегестрироваться</button>
    </form>
{% endblock content %}
```

### Шаг 8. Описание URLs
В ```project/urls.py``` занесем информацию, какое приложение для чего будет использовано:
```
from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", include("users.urls")), # для передачи управления SignUp
    path("users/", include("django.contrib.auth.urls")), # Для реализации login/logout/passwordchange/passwordreset
    path("", include("users.urls")) # HomeView будет реализован тоже в приложении Users (потом уберем)
]
```

В приложении ```users/urls.py```:
```
from django.urls import path 
from .views import SignUpView, HomePageView 


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("", HomePageView.as_view(), name = "home"),
]
```
### Шаг 9. Настройка отображений
Теперь необходимо связать все в один клубок
```users/views.py```:
```
from django.views.generic import CreateView, TemplateView
# Create your views here.
from .forms import MyUserCreationForm
from django.urls import reverse_lazy

class SignUpView(CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html' 


class HomePageView(TemplateView):
    template_name = 'home.html' 
```