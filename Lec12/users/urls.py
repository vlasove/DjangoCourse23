from django.urls import path 
from .views import SignUpView, HomePageView 


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("", HomePageView.as_view(), name = "home"),
]
