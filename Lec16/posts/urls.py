from django.urls import path 
from .views import PostsListView , PostEditView, PostDetailView, PostDeleteView, PostCreateView

urlpatterns = [
    path("", PostsListView.as_view(), name="list_posts"),
    path("new/", PostCreateView.as_view(), name="new_post"),
    path("<int:pk>/edit/", PostEditView.as_view(), name="edit_post"),
    path("<int:pk>/", PostDetailView.as_view(), name="detail_post"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="delete_post")
]