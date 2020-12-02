from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
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

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "delete_post.html"
    success_url = reverse_lazy("list_posts")
    login_url = 'login'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post 
    template_name = "new_post.html"
    fields = ("title", "body")
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user#Singleton pattern
        return super().form_valid(form)

