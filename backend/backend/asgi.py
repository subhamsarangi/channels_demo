import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from tasks.routing import websocket_urlpatterns as ws_tasks
from chat.routing import websocket_urlpatterns as ws_chat

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

ws_patterns = ws_tasks + ws_chat


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(ws_patterns)),
    }
)
