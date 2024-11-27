from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ninja import Router, NinjaAPI

from .models import ChatRoom, ChatRoomMembership
from .mongo_models import Message
from apps.myauth.models import User

chat_api = NinjaAPI(urls_namespace="chat")
chat_router = Router()
chat_api.add_router("", chat_router)


@chat_router.get("")
@login_required
def chat(request):
    return render(request, "chat/chat.html")


@chat_router.get("/{room_name}")
@login_required
def chat_room(request, room_name: str):
    chat_room = ChatRoom.objects.filter(name=room_name).first()

    if not chat_room:
        return render(request, "chat/chat_room.html", {"room_name": room_name})

    members = ChatRoomMembership.objects.filter(chat_room=chat_room).select_related(
        "user"
    )

    messages = Message.objects.filter(chat_room=chat_room.id).order_by("created_at")

    formatted_messages = [
        {
            "user": User.objects.get(id=msg.user).full_name,
            "content": msg.content,
            "created_at": msg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for msg in messages
    ]

    return render(
        request,
        "chat/chat_room.html",
        {
            "room_name": room_name,
            "members": members,
            "chat_messages": formatted_messages,
        },
    )
