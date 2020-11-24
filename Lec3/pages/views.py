# from django.shortcuts import render
"""
Импортируем стандартные сущности для создания ответа на запрос
"""
from django.http import HttpRequest, HttpResponse

# Create your views here.
def homePageView(request:HttpRequest):
    """
    Функция которая будет отображать Hello world!
    на веб странице. HttpResponse встроит ваш текст в стандартный внутренний шаблон
    """
    return HttpResponse("<h1>Hello world!</h1>")
