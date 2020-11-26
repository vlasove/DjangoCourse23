from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    # В поле автора мы помещаем реляцию со стандартной пользовательской моделью Django
    # auth.User - стандартный юзер в Django
    # Создаем соотношение ONE-TO-MANY (по отношению к автору)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return "Title: " + self.title
