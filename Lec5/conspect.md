## Лекция 5. Что было недосказано в лекции 4.
Скопируем из лекции 4 следующие компоненты:
* ```pages```
* ```project```
* ```templates```
* ```db.sqlite3, manage,py```
* ```pipenv``` сделали заново

Проблема: когда веб страниц в приложении становится много, следить за работоспособностью каждой из них становится все сложнее и сложнее.

***Решение:*** создадим набор тестов, который будет проверять доступность каждой веб-страницы нашего приложения.

### Шаг 1. Заходим в ```pages/test.py```
Наша задача - проверить, возможно ли остуществить ```GET``` запрос для каждой страницы нашего приложения. Давайте напишем по одному тесту на каждый запрос:
* тест включает в себя имитацию ```GET``` запроса к странице
* тест проверяет, что запрос был выполнен с кодом ```200```
* Подробнее рекомендуется почитать про устройство ***HTTP/HTTPS** протоколов(конкретнее - HTTP verbs, HTTP status codes).

Пропишем в ```pages/tests.py```:
```
from django.test import SimpleTestCase
"""
SimpleTestCase - используем потому, что не задействована база данных
"""
# Create your tests here.
class PagesTests(SimpleTestCase):
    def test_homepage_status_code(self):
        response = self.client.get('/') 
        self.assertEqual(response.status_code, 200)

    def test_aboutpage_status_code(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200) 

```

А теперь запустим при помощи ```python manage.py test```


## Добавим новую страницу Info
#### Ресурс для изучения HTML/CSS
***Ссылка***: https://www.freecodecamp.org/learn

* Сначала напишем тест :
```
def test_infopage_status_code(self):
        response = self.client.get("/info/")
        self.assertEqual(response.status_code, 200) 
```
* Затем создадим шаблон ```templates/info.html```
```
<!--templates/info.html-->
{% extends 'base.html'%}

{% block content %}
<h1>Info page</h1>
<p>
    This is new info page for my micro application!
</p>
{% endblock content %}
```
* Добавим новый ```view```
```

class InfoPageView(TemplateView):
    """
    Для отображения странички info
    """
    template_name = 'info.html'
```
* Исправим ```pages/urls.py```
```
urlpatterns = [
    path("info/", InfoPageView.as_view(), name='info'),
    path("about/", AboutPageView.as_view(), name='about'),
    path("", HomePageView.as_view(), name='home'),
]
```
* Добавим плашу info в нашу навигацию:
```
<!--templates/base.html-->
<header>
    <a href="{% url 'home' %}">Home</a> 
    |
    <a href="{% url 'about' %}">About</a>
    |
    <a href="{% url 'info' %}">Info</a>
</header>

{% block content %}
{% endblock content %}
```