import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "youcars.settings")

import django
django.setup()

from django.core.asgi import get_asgi_application
from websoket import routing
from websoket.middleware import JWTAuthMiddleWare
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": JWTAuthMiddleWare(
            URLRouter(routing.websocket_urlpatterns),
        ),
    }
)
