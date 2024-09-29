from django.urls import path
from .consumers import ProgressConsumer, ClockConsumer

websocket_urlpatterns = [
    path('ws/progress/', ProgressConsumer.as_asgi()),
    path('ws/clock/', ClockConsumer.as_asgi()),
]
