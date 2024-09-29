# SETTING UP TO USE Channels

### install

`pip install django daphne channels`

### create project and app

```bash
django-admin startproject my_project
cd my_project
python manage.py startapp my_app
```

### settings file

```py
INSTALLED_APPS = [
    # default apps
    'channels',
    'my_app'
]

ASGI_APPLICATION = 'my_project.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}
```

### a consumer file inside my_app

```py
import asyncio
from datetime import datetime
import json

from channels.generic.websocket import AsyncWebsocketConsumer

class ClockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        while True:
            await asyncio.sleep(2)  # Simulate waiting
            await self.send(json.dumps({
                'clock': str(datetime.now())
            }))
```

### a routing file inside my_app

```py
from django.urls import path
from .consumers import ClockConsumer

websocket_urlpatterns = [
    path('ws/clock/', ClockConsumer.as_asgi()),
]
```

### asgi file

```py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from my_app.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
```
