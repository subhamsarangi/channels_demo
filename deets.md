# SETTING UP TO USE Channels

### install channels along with django

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

### If you want HTTP/2 support and TLS support

- run `poetry add Twisted[http2,tls]`

#### there are other steps to make use of TLS

- make key: `openssl genrsa -out privatekey.pem 2048`

- make certificate `openssl req -new -x509 -key privatekey.pem -out cert.pem -days 365`

- run daphne with the keys: `daphne -b 0.0.0.0 -e ssl:8001:privateKey=privatekey.pem:certKey=cert.pem progress_app.asgi:application`

### Chat

#### add psycopg2-binary and python-dotenv

`poetry add psycopg2-binary python-dotenv`

#### make a .env file
```sh
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=chatdb
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```