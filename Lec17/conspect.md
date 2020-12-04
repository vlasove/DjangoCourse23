## Лекция 17. Перенос на сервер и генерация документации

***Проблема:*** на данный момент проект работает, выполняет все необходимые функции и имеет необходимую поддержку аккаунтов пользователя. Но мы бы хотели,
чтобы наш проект стал доступен всем. Для этого необходимо весь проект перенсти на хостинг. Где хостинг взять? И как переносить?

***Задача:*** перенести проект ```Django``` на хостинг.
В качестве учебного хостинга возьмем ```ngrok```. В качестве хост-машины будем использовать данную ОС. ```ngrok``` сгенерирует нам необходимые ```host``` и ```domen```.

## Шаг 1. Получим и отконфигурируем утилиту ngrok
* Заходим на сайт ```https://ngrok.com/``` 
* Регистрируемся на сайте
* После успешной регистрации скачаем саму утилиту ```ngrok``` : ```https://bin.equinox.io/c/.../ngrok-stable-windows-amd64.zip```
* После скачивания поместим ```ngrok.exe``` (находится в скачанном архиве) в проектную директорию.
* Теперь отконфигурирем ```ngrok.exe``` в соответствии с вами ```auth_token```
* В командной строке пропишем ```ngrok authtoken <your-aurh-roken>```
* Теперь у нас есть отконфигурированный ```host```.

## Шаг 2. Подготовим проект Django для переноса на host
В файле ```settings.py``` -> ```ALLOWED_HOSTS = ["*"]``` . Теперь наш проект может быть перенес на абсолютно любой хостинг, какой мы только ему предложим.

## Шаг 3. Запуск и связывание портов.
Для того, чтобы сгенерировать хост и домен при помощи ```ngrok``` необходимо выполнить 2 условия:
* Порт, который будет привязан к ```ngrok``` должен совпадать с портом локального хоста, где запускается сам проект (у нас в проекте ```8000```)
* Получим выбитый хост и попробуем протестировать проект

Запускаем ```ngrok``` командной : ```ngrok http 8000``` . Теперь нам доступно 2 адреса (2 хоста):
* ```http://...```
* ```https://...```

## Шаг 4. Проверка, что все работает
Попробуем перейти на выбитый хост ```https://1b688f47f592.ngrok.io```. Все должно быть ок!

## Шаг 5. Отключим Debug
Не хотим, чтобы пользователь, видел все кишки наших запросов при неудачном ```url-request```. Для этого в ```settings.py``` -> ```DEBUG = False``` . ***Важно помнить*** : что если вы отключаете опцию ```DEBUG``` обязательно следует указать набор доступных ```host```'ов, т.к. ```Django``` (после отключения Debug) начинает думать, что это ```production deploy```.


## Как причесать проект?
Существует стандарт ```PEP8``` , которого необходимо придерживаться при написании программного кода.  Для причесывания кода есть 2 варианта:
* Открываем документацию ```PEP8``` и вручную переверстываем все модули в проекте (путь настоящего мужика!)
* Будем использовать утилиту, которая автоматически проверит и ***ИСПРАВИТ*** все недочеты в коде в соответствии с стандартом ```PEP8``` => данна яутилита называется линтер. 
В Python самые популярные линтеры это:
* ```autopep8``` (по умолчанию достаточно мягкий, может на месте изменять все недочеты)
* ```flake8``` (более агрессивный, имеет функционал ```in-place``` изменений, достаточно удобная конфигурация)
* ```pylint``` (***УЛЬТРА-АГРЕССИВНОЕ СУЩЕСТВО*** , самый консервативный линтер, проверяет все до символа (по умолчанию), не имеет встроенного функционала для ```in-place```)

Для начала рекомендуется освоить ```autopep8```. 
Для того, чтобы установить ```autopep8``` : ```pip install autopep8``` (рекомендуется установить его под ОС)
После чего запустим ```autopep8``` для всего проекта:
* Перейдем в проектную директорию (в нашем случае ```Lec17```)
* Выполним команду ```autopep8 . --recursive --aggressive --in-place --verbose```
* Если хотим запустить ```autopep8``` для какого-то отдельного ***приложения*** : ```autopep8 <application_name> --recursive --aggressive --in-place --verbose```

***Рекомендуется ознакомиться*** как в аналогичном стиле запустить ```flake8``` и ```pylint```.

## Как сгенерировать документацию?
В сообществе ```Python``` существует единый инструмент , для генерации документации кода (в виде ```html_template```) : ```SPHINX```.
* Установим ```sphinx```: ```pip install sphinx```.

Для того, чтобы подключить автогенерацию документации нашего проекта выполним команду ```sphinx-quickstart```.
После заполнения необходимых полей (```n```, ```Django Blog Project```, ```Evgeny Vlasov``` , ```1.0.0```) заходим в файл ```conf.py``` и подсоединим инструмент генерации документации к нашему ***проекту***.
```
#conf.py
.....
import os
import sys
import django
sys.path.insert(0, os.path.abspath('.'))
os.environ["DJANGO_SETTINGS_MODULE"] = "project.settings" # Путь до settings проекта
django.setup()
...
```

После чего выполним команду для генерации документации текущего проекта ```sphinx-apidoc -o . ..```
* ***Рекомендуется*** локально установить (под ОС) ```pip install django-crispy-forms```
После чего попросим сгенерировать документы в формате ```html```:
```make html```
Если в ОС есть стандартный комплиятор ```pdf``` файлов то сделать документацию в формате pdf можно 2-мя способами:
* ```pip install rst2pdf``` -> ```rst2pdf index.rst index.pdf```
* ```make pdf```

После чего ***обязательно*** причешите весь код в соответствии с ```pylint``` (добавить ***ВЕЗДЕ*** ```docstrings```) и выполнить все те же самые дейсвтия повторно - в результата на странице ```index.html``` вы увидите все необходимые описания ***ИЛИ*** добавить документацию вручную.