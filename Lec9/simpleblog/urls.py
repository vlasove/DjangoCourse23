from django.urls import path 

from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="delete_post"),  # форма для удаления поста
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name = 'update_post'), # view для отображения формы update


    path('post/create/', PostCreateView.as_view(), name = 'create_post'), # Добавляем view для отображения формы создания Поста
    path("post/<int:pk>/", PostDetailView.as_view(), name="detail_post"), #post/1 pk == id из модели 
    path("", PostListView.as_view(), name="home"),
]