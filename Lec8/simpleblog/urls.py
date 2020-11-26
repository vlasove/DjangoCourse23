from django.urls import path 

from .views import PostListView, PostDetailView

urlpatterns = [
    path("post/<int:pk>", PostDetailView.as_view(), name="detail_post"), #post/1 pk == id из модели 
    path("", PostListView.as_view(), name="home"),
]