from django.urls import path 

from .views import HomePageView, AboutPageView

urlpatterns = [
    path("about/", AboutPageView.as_view()),
    path("", HomePageView.as_view()),
]