from django.shortcuts import render

from ninja import Router, NinjaAPI

chat_api = NinjaAPI(urls_namespace="chat")
chat_router = Router()
chat_api.add_router("", chat_router)


@chat_router.get("")
def chat(request):
    return render(request, "chat/chat.html")


@chat_router.get("/{room_name}")
def chat_room(request, room_name: str):
    return render(request, "chat/chat_room.html", {"room_name": room_name})
