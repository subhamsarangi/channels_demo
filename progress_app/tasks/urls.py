from django.urls import path
from .views import index, game

urlpatterns = [
    path('', index, name='index'),
    path('game/', game, name='game'),
]
