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

class AboutPageView(TemplateView):
    """
    Для отображения странички about
    """
    template_name = "about.html"

class InfoPageView(TemplateView):
    """
    Для отображения странички info
    """
    template_name = 'info.html'