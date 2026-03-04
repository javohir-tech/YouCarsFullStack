from django.urls import re_path
from .consumers import ChatConsumer , ConversationsConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<user_id>[0-9a-fA-F-]+)/$" , ChatConsumer.as_asgi()),
    re_path("ws/conversations/" , ConversationsConsumer.as_asgi())
]