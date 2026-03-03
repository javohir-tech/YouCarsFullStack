from django.urls import path
from .views import GetChathistory

urlpatterns = [
    path("chat/<uuid:pk>/history/", GetChathistory.as_view()),
]
