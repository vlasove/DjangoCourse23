from .views import homePageView

"""
функция для сопоставления url ссылки с отображением
"""
from django.urls import path

# Создадим стандартную паллету (паттерн) сопоставления url ссылок с отображениями
# urlpatterns - стандартное имя
urlpatterns = [
    path("", homePageView),
]