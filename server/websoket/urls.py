from django.urls import path
from .views import GetChathistory, ConversationListView

urlpatterns = [
    path("chat/<uuid:pk>/history/", GetChathistory.as_view()),
    path("conversations/", ConversationListView.as_view()),
]
