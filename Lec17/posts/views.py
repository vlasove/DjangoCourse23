from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
# Исключение, ответств за разгр прав доступа
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post

#   PostDeleteView
# Create your views here.


class PostsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "list_posts.html"
    context_object_name = "posts"
    login_url = 'login'


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "detail_post.html"
    context_object_name = "post"
    login_url = 'login'


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "edit_post.html"
    fields = ("title", "body")
    context_object_name = "post"
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        """
        /posts/1/edit/ при переходе , например, по данной ссылке отрабатывает следующая последовательность действий:
        * вызывается отображение PostEditView.as_view()
        * затем вызывает метод dispatch()
        * если dispatch() не провоцирует исключений - получаем доступ к запросу, показываем шаблон, заполняем форму
        * если dispatch() кидает исключение - валимся с 403 ошибкой
        """
        post_object = self.get_object()  # Post на странице
        if post_object.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "delete_post.html"
    success_url = reverse_lazy("list_posts")
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        """
        /posts/1/delete/ при переходе , например, по данной ссылке отрабатывает следующая последовательность действий:
        * вызывается отображение PostDeleteView.as_view()
        * затем вызывает метод dispatch()
        * если dispatch() не провоцирует исключений - получаем доступ к запросу, показываем шаблон, заполняем форму
        * если dispatch() кидает исключение - валимся с 403 ошибкой
        """
        post_object = self.get_object()  # Post на странице
        if post_object.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "new_post.html"
    fields = ("title", "body")
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user  # Singleton pattern
        return super().form_valid(form)
