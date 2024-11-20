from django.shortcuts import render
from django.conf import settings
from ninja import Router, NinjaAPI

from backend.utils import restrict_ip

tasks_api = NinjaAPI(urls_namespace="tasks")
tasks_router = Router()
tasks_api.add_router("", tasks_router)


@tasks_router.get("")
# @restrict_ip(settings.TRUSTED_ADMIN_IP)
def index(request):
    return render(request, "tasks/index.html")


@tasks_router.get("/game")
def game(request):
    return render(request, "tasks/game.html")
