from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.urls import reverse_lazy
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

class PostCreateView(CreateView):
    """
    Класс для отображения веб-формы создания поста.
    Для корректного оторражения требуется указание модели, шаблона, название отображаемых полей
    """
    model = Post 
    template_name = 'create_post.html'
    fields = '__all__' # Пока отображаем все поля в веб-форме (исключается только id)

class PostUpdateView(UpdateView):
    """
    Класс для отображения веб-формы обновления поста.
    Для корректного отображения требуется указание модели, шаблона, название отображаемых полей
    """
    model = Post 
    template_name = 'update_post.html'
    fields = ["title", "content"] # Не хотим , чтобы юзер мог поменять автора поста, а title и content - ок!

class PostDeleteView(DeleteView):
    """
    Класс для отображения веб-формы удаления поста.
    Для корректного отображения требуется указание модели, шаблона, КУДА перенаправлять после удаления
    """
    model = Post 
    template_name = 'delete_post.html'
    success_url = reverse_lazy("home") # Редирект выполняется ПОСЛЕ нажатия на кнопку `submit`. Обычный reverse() выполнился бы ДО.