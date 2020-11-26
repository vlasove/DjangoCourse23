from django.views.generic import ListView 

from .models import Post 

# Create your views here.
class HomePageView(ListView):
    # какие объекты мы хотим отображать списком
    model = Post
    template_name = 'home.html'
    # Имя, под которым в шаблоне будут доступны списки постов
    context_object_name = 'posts'