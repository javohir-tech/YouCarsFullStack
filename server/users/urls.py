from django.urls import path
from .views import (
    SingUpView,
    LoginView,
    LogOutView,
    ForgetPasswordView,
    CodeVerifyView,
    NewPasswordView,
    EditEmailView,
    EmailVerifyView,
    UpdateUserView,
    UpdatePasswordView,
    GetUserView,
    LoginRefreshView, 
    UserImageDelete
)

# app_name = 'users'

urlpatterns = [
    path("singup/", SingUpView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogOutView.as_view()),
    path("forget/", ForgetPasswordView.as_view()),
    path("verify/", CodeVerifyView.as_view()),
    path("new_password/", NewPasswordView.as_view()),
    path("email/", EditEmailView.as_view()),
    path("email/verify/", EmailVerifyView.as_view()),
    path("user/update/", UpdateUserView.as_view()),
    path("password/update/", UpdatePasswordView.as_view()),
    path("user/", GetUserView.as_view()),
    path("refresh/" , LoginRefreshView.as_view()), 
    path("user/image/delete/<uuid:pk>" , UserImageDelete.as_view())
]
