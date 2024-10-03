from django.urls import path
from .views import index, game

app_name = "tasks"
urlpatterns = [
    path("", index, name="index"),
    path("game/", game, name="game"),
]
