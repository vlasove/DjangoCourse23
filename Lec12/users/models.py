from django.db import models
# Импортируем абстрактного пользователя
from django.contrib.auth.models import AbstractUser

# Create your models here.
class MyUser(AbstractUser):
    age = models.IntegerField(null=True, blank=True) # null - это означает, что в базе данных, в случае не указания возраста будет стоять NULL
                                                     # blank - допускается создание ОБЪЕКТА MyUser без указания age - информация для валидации форм
                                                     
