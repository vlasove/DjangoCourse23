from django.views.generic import ListView, DetailView
from .models import Post
# Create your views here.

class PostListView(ListView):
    """
    Класс для отображения набора постов. Набор постов адресуется шаблону home.html
    Внутри шаблона набор постов доступен по имени `posts`
    """
    model = Post 
    template_name = "home.html"
    context_object_name = "posts"

class PostDetailView(DetailView):
    """
    Класс для детального отображения поста. Пост адресуется шаблону detail_post.html
    Внутри шаблона пост доступен по имени `post`
    """
    model = Post 
    template_name = "detail_post.html"
    context_object_name = "post"

