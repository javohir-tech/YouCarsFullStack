from django.urls import path
from .views import SingUpView, LoginView, LogOutView

urlpatterns = [
    path("singup/", SingUpView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogOutView.as_view()),
]
