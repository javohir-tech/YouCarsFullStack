import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youcars.settings')

from websoket import routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter , URLRouter


application = ProtocolTypeRouter({
    'http' : get_asgi_application(), 
    'websocket' :AuthMiddlewareStack(
        URLRouter(routing.websocket_urlpatterns)
    ),
})
