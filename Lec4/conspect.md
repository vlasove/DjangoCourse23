## Лекция 4. Создаем многостраничное приложение
По началу:
* ```pipenv shell```
* ```pipenv install django```
* ```django-admin startproject project .```
* ```python manage.py startapp pages```

Где ```project``` - ядро проект (сам проект), ```pages``` - приложение, которое будет отображать несколько веб-страниц.

#### Шаг 1. Регистрируем приложения для проекта
```settings.py``` - > ```INSTALLED_APPS``` -> добавляем ```pages.apps.PagesConfig```

#### Шаг 2. Создадим шаблоны (templates) для отображения
Для этого необходимо выполнить следующие шаги:
* внутри приложения ```pages``` создадим директорию ```templates```
* внутри ```templates``` создадим директорию ```pages```
* внутри ```templates/pages``` создам файл ```home.html```
* необходимо сообщить нашему проекту ГДЕ ТЕПЕРЬ ИСКАТЬ ШАБЛОНЫ?
* для этого заходим ```settings.py``` - > ```TEMPLATES``` и прописываем
```'DIRS': [os.path.join(BASE_DIR, 'templates')]``` (не забудем импортирвоать ```import os```) - это общий путь
* ***Из-за того, что пока у нас будет всего 1 приложение***, можно складывать шаблоны даже в корень (вытащим директорию ```templates``` на уровень проекта (рядом с ```manage.py```))

Создаем шаблон ```home.html```:
```
<!-- templates/home.html ЭТО КОММЕНАТРИЙ-->
<h1>My Homepage</h1>
```

#### После создания шаблона прописываем логику отображения
Нужно ответить на вопрос : когда его показывать? На это ответит
```views.py```.

Внутри ```views.py```:
```
from django.views.generic import TemplateView
"""
TemplateView - встроенный класс для оторажения простых шаблонов
"""

# Create your views here.
class HomePageView(TemplateView):
    """
    класс-отображение (Class-Based View) - способ создания отображения,
    учитывающий как статику, так и динамику
    """
    template_name = "home.html"
```

Теперь в ```pages/urls.py``` необходимо передать управление отображению ```HomePageView```:
```
from django.urls import path 

from .views import HomePageView

urlpatterns = [
    path("", HomePageView.as_view()),
]
```
Метод ```.as_view()``` нужен, для того, чтобы вызвать родительский метод, способный отображать ```HttpResponse``` на основе настроек дочернего класса.

#### После этого
Пердадим управление нашему приложению из проекта:
```
#project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("pages.urls")),
]
```

***После этого проверим, что все работает*** : ```python manage.py runserver``` 

## Теперь создадим вторую страницу About
Задача: создать вторую страничку ```about```.

Создаем шаблон ```about.html```:
```
<!--templates/about.html-->
<h1>About page</h1>
```

#### После создания шаблона прописываем логику отображения
Нужно ответить на вопрос : когда его показывать? На это ответит
```views.py```.

Внутри ```views.py```:
```
from django.views.generic import TemplateView
"""
TemplateView - встроенный класс для оторажения простых шаблонов
"""

# Create your views here.
class HomePageView(TemplateView):
        ....

class AboutPageView(TemplateView):
    """
    класс-отображение (Class-Based View) - способ создания отображения,
    учитывающий как статику, так и динамику
    """
    template_name = "about.html"
```


Теперь в ```pages/urls.py``` необходимо передать управление отображению ```AboutPageView```:
```
from django.urls import path 

from .views import HomePageView

urlpatterns = [
    path("about/", AboutPageView.as_view()),
    path("", HomePageView.as_view()),
]
```

## Проблема - отстуствие навигации.
Создадим родительский шаблон, который будет обладать информацией про
существующие в приложении страницы. Для этого создадим шаблон ```base.html```:
```
<!--templates.base.html-->
<header>
    <a href="">Home</a> 
    |
    <a href="">About</a>
</header>

{% block content %}
{% endblock content %}

```

Синтаксис {% ... %} - специфический синтаксис встроенного шаблонизатора ```Jinja2```. Перепишем дочерний шаблон ```home.html```:
```
<!-- templates/home.html ЭТО КОММЕНАТРИЙ-->
{% extends 'base.html' %}

{% block content %}
<h1>My Homepage</h1>
{% endblock content %}
```
А также ```about.html```:
```
<!--templates/about.html-->
{% extends 'base.html' %}

{% block content %}
<h1>About page</h1>
{% endblock content%}
```
## Для решения проблемы динамической линковки добавим url-ники
В ```pages/urls.py``` введем имена для каждого запроса:
```
from django.urls import path 

from .views import HomePageView, AboutPageView

urlpatterns = [
    path("about/", AboutPageView.as_view(), name='about'),
    path("", HomePageView.as_view(), name='home'),
]
```

А теперь воспользуемся никами в базовом шаблоне:
```
<!--templates.base.html-->
<header>
    <a href="{% url 'home' %}">Home</a> 
    |
    <a href="{% url 'about' %}">About</a>
</header>

{% block content %}
{% endblock content %}
```

