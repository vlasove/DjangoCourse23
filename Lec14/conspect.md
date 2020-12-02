## Лекция 14. Механизмы сброса и изменения пароля

***Задача:*** при использовании стандартного приложения ```django.contrib.auth``` в приложении ```users``` отстуствует надобность в прямой (низкоуровневной) реализации функционала сброса пароля.
***Проблема:*** стандартаные ```Django``` стандартные шаблоны для отображения ```views``` по адресам:
```
users/ password_change/ [name='password_change']
users/ password_change/done/ [name='password_change_done']
users/ password_reset/ [name='password_reset']
users/ password_reset/done/ [name='password_reset_done']
```
притянуты из панели администратора. Нас не устраивает.

***Решение:*** создадим свои шаблоны , которые соответствуют необходимым ```url``` адресам.

### Шаг 1. Изменение пароля пользователя
Для исправления отображения страниц с ***изменением*** пароля нам необходимо создать свои шаблоны, которые будут отображаться в результате перехода по ссылкам:
```
users/ password_change/ 
users/ password_change/done/
```
Создаем шаблон ```templates/registration/password_change_form.html``` для того, чтобы он был захвачен стандартным ```views``` и показан пользователю при переходе по ссылке ```users/ password_change/ ```:
```
<!--templates/registration/password_change_form-->
{% extends 'base.html' %}

{% load crispy_forms_tags %}

{% block content %}
    <h1>Password change</h1>
    <p>Enter old password, then for security, enter your new password twice.</p>
    <form method="post">
        {% csrf_token %}
        {{ form|crispy }}
        <button class="btn btn-success ml-2" type="submit">Change password</button>
    </form>
{% endblock content %}
```
После верстки данного шаблона залогинемся на сайте под каким-нибудь пользователем и попробуем перейти на страницу ```/users/password_change/``` . В случае, если все ок - должны увидеть форму с 3 полями.

***Теперь*** сверстаем шаблон успешного подтверждения измнения пароля (на эту страницу мы будем перенаправлены автоматически после заполнения формы ```password_change```). Данный шаблон будет отображаться при переходе на ссылку ```/users/password_change/done/```. Данный шаблон называется ```templates/registration/password_change_done.html```:
```
<!--templates/registration/password_change_done.html-->
{% extends 'base.html' %}

{% block content %}
    <h1>Password change successfully</h1>
    <p>Your password was changed.</p>
{% endblock content %}
```

***Попробуйте самостоятельно*** : реализуйте простейшую логику. Пользователь заходит на страницу ```users/password_change/```. Допусти он успешно сменил пароль => его автоматически перенаправляет на страницу ```users/password_change/done```. Реализуйте функционал, который бы через ***5 секунд*** перенаправлял пользователя на домашнюю страницу.

### Шаг 2. Сброс пароля пользователя
Для успешного сброса пароля нам необходимо решить 3 проблемы:
* Как ***генерировать*** ссылку для сброса пароля? Эта ссылка должна перенаправлять нас на страницу ```/users/password_reset/``` именно для ***текущего*** пользователя.
* Что делать с паролем (текущим) , если пользователь перешел по ссылку, *** но пароль не менял***?
* Куда отправлять эту ***магическую*** ссылку?

### Шаг 2.1. Связь лога отправки с консолью
Для того, чтобы при разработке приложения мы могли проследить валидность создания ссылки для сброса пароля пользователя, нам нужно ег окак-то получать.
Сообщим ```Django``` , что мы хотим получать эту ссылку самым простым способом - пусть она выпадает в консоль.
Для того, чтобы реализовать такую логику, необходимо зайти в ```settings.py``` и найти\создать поле ```EMAIL_BACKEND```.
```
# Куда отправлять сообщения по сбросу пароля
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
Попробуем протестировать функционал. Для этого перейдем на страницу ```users/password_rest/``` введем ```email``` адрес нашего пользователя и нажем ```reset my password```. Для начала исправим способ взаимодействия с моделью ```users/forms.py```:
```
# Это именно низкоуровневые интерфейсы взаимодействия с моделью
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import MyUser

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser 
        fields = ('username', 'email', 'age')

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = MyUser
        fields =  ('username', 'email', 'age') 
```
Теперь нам необходимо указывать ```email``` адрес при регистрации.

Давайте теперь зарегестрируем какого-нибудь нового пользователя с ```email``` адресом. После чего перейдем на страницу ```users/password_reset/``` введем ранее описаный ```email``` адрес и увидим в консоли сообщение с примерным содержанием:
```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 8bit
Subject: Password reset on localhost:8000
From: webmaster@localhost
To: test@gmail.com
Date: Wed, 02 Dec 2020 16:17:58 -0000
Message-ID: <160692587857.6596.15507907595915258530@B01-TEACHER>


You're receiving this email because you requested a password reset for your user account at localhost:8000.

Please go to the following page and choose a new password:

http://localhost:8000/users/reset/Mw/ae9ply-0af91c24f3504583d2f89113bc5f823a/

Your username, in case you’ve forgotten: test

Thanks for using our site!

The localhost:8000 team

```
### Шаг 2.2. Создание наших шаблонов для сброса пароля
Для того, чтобы првоести пользователя по схеме сброса пароля необходимо реализовать 4 шаблона:
```
templates/registration/password_reset_form.html
templates/registration/password_reset_done.html
templates/registration/password_reset_confirm.html
templates/registration/password_reset_complete.html
```

Начнем с ```templates/registration/password_reset_form.html```:
```
<!--templates/registration/password_reset_form.html-->
{% extends 'base.html' %}
<!--Данная форма отображается при запросе, на котором первично вводится адрес электронной почты-->
{% load crispy_forms_tags %}

{% block content %}
    <h1>Forgot password?</h1>
    <p>Enter your email address and we will send you instructions for password resetting</p>
    <form method="post">
        {% csrf_token %}
        {{ form|crispy }}
        <button class="btn btn-success ml-2" type="submit">Send Instructions</button>
    </form>
{% endblock content %}
```

Теперь ```templates/registration/password_reset_done.html```:
```
<!--templates/registration/password_reset_done.html-->
{% extends 'base.html' %}

{% block content %}
    <h1>Check your inbox :)</h1>
    <p>We've emailed you instructions for password resetting.</p>
{% endblock content %}
```

Теперь страница ввода нового праоля в 2-ух экземплярах ```templates/registration/password_reset_confirm.html```:
```
<!--templates/registration/password_reset_confirm.html-->
{% extends 'base.html' %}

{% load crispy_forms_tags %}

{% block content %}
    <h1>Set new password</h1>
    <form method="post">
        {% csrf_token %}
        {{ form|crispy }}
        <button class="btn btn-success ml-2" type="submit">Set password</button>
    </form>
{% endblock content %}
```

Последний пункт ```templates/registration/password_reset_complete.html```:
```
<!--templates/registration/password_reset_complete.html-->
{% extends 'base.html' %}

{% block content %}
    <h1>Password reset complete</h1>
    <p>
        Your new password has benn set.Try login now <a href="{% url 'login' %}">LogIn page</a>.
    </p>
{% endblock content
```


***Ядро функционала пользователя*** состоит из стандартных механизмов:
* LogIn
* LogOut
* SignUp
* Password Change
* Password Reset

Данное ядро будет сопровождать все ваши будущие приложения на ```Django``` :)