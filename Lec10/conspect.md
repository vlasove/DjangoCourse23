## Лекция 10. Модульные тесты для приложения

До сих пор мы не писали тесты для нового приложения с постами. Пора исправить этот недочет. 
В подходе ```TDD``` принято писать модульные тесты для приложения еще ***ДО МОМЕНТА*** реализации всего ключевого функционала.

Тестируем приложение ```simpleblog```. Работаем в модуле ```simpleblog/tests.py```.

### Шаг 1. Глобальный setUp
Перед тем, как мы начнем использовать сценарии тестирования необходимо подготовить тестовую базу.
Подготовка заключается в :
* создание 1 пользователя
* создание 1 поста

```
def setUp(self):
        # 1 Определяем пользователя и добавляем его в тестовую БД
        self.current_user = get_user_model().objects.create_user(
            username = 'test',
            email = 'test@test.com',
            password = 'secretpassword9000',
        )

        # 2. Определим пост, созданный тестовым пользователем
        self.current_post = Post.objects.create(
            title = 'Test title',
            content = 'Test content',
            author = self.current_user,
        )
```

### Шаг 2. Проверим, что при создании поста, корректно отображается его строковое представление
Что будет, если применить функцию ```str()``` к любому объекту класса ```Post```?
Что будет, если вызвать метод ```get_absolute_url``` у тестового поста?
```
    def test_str_method_for_model(self):
        """
        Тест для строкового представления объекта модели Post
        """ 
        post = Post(title='Test title')
        self.assertEqual(str(post), 'Title: Test title')

    def test_get_absolute_url(self):
        """
        Тест для метода модели get_absolute_url
        """
        self.assertEqual(self.current_post.get_absolute_url(), "/post/1/")
```


### Шаг 3. Проверим, что пост создался с корректными атрибутами
```
 def test_post_creation_object(self):
        """
        Тест для проверки правильного заполенения атрибутов объекта класса Post
        """
        self.assertEqual(str(self.current_post.title), 'Test title')
        self.assertEqual(str(self.current_post.content), 'Test content')
        self.assertEqual(str(self.current_post.author), 'test')
```

### Шаг 4. Проверка валидности отображения домашней страницы

Проверяет доступность домашней страницы по пути "/" , а также по нику "home"
Проверяет, что на странице присутствует как минимум 1 пост.
```
def test_homepage_list_view(self):
        """
        Проверяет доступность домашней страницы по пути "/" , а также по нику "home"
        Проверяет, что на странице присутствует как минимум 1 пост.
        """
        response_abs = self.client.get("/")
        self.assertEqual(response_abs.status_code, 200)

        response_name = self.client.get(reverse("home"))
        self.assertEqual(response_name.status_code, 200)

        # Блок првоерки содержимого
        self.assertContains(response_name, 'Test content')
        self.assertTemplateUsed(response_name, "home.html")

```

### Шаг 5. Проверка, что детальное отображение поста работает корректно
Проверяет, что ```post/1``` существует
Проверяет, что других постов нет, например post/20 не существует
Проверяет , что контент страницы содержит наш пост
Проверяет, что отображается правильный шаблон
```
def test_detail_post_view(self):
        """
        Проверяет, что post/1 существует
        Проверяет, что других постов нет, например post/20 не существует
        Проверяет , что контент страницы содержит наш пост
        Проверяет, что отображается правильный шаблон
        """
        response_abs = self.client.get("/post/1/")
        self.assertEqual(response_abs.status_code, 200)

        response_name = self.client.get(reverse("detail_post", args=[str(1)]))
        self.assertEqual(response_name.status_code, 200)

        no_response = self.client.get("/post/20/")
        self.assertNotEqual(no_response.status_code, 200)

        self.assertContains(response_name, 'Test content')
        self.assertTemplateUsed(response_name, "detail_post.html")
```

### Шаг 6. Проверка обновления
Проверяет, что при обновлении поста происходит редирект на другую страницу
```
def test_update_post_view(self):
        """
        Проверяет, что при обновлении поста происходит редирект на другую страницу
        """ 
        response = self.client.post(reverse("update_post", args=[str(1)]), { 
            'title' : 'Test title updated',
            'content' : 'Test content updated',
        })
        self.assertEqual(response.status_code, 302)
```

### Шаг 7. Проверка удаления
Проверка удаления
```
def test_delete_post_view(self):
        """
        Проверка удаления
        """ 
        response = self.client.get(
            reverse("delete_post", args=[str(1)])
        )
        self.assertEqual(response.status_code, 200)
```

### Шаг 8. Проверка создания поста
Проверяет, что созданный объект корректен и корректно отображается
```
def test_create_post_view(self):
        """
        Проверяет, что созданный объект корректен и корректно отображается
        """
        response = self.client.post(
            reverse('create_post') ,
            {
                'title' : 'New test title',
                'content' : 'New test content',
                'author' : self.current_user,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New test title')
        self.assertContains(response,'New test content')
```