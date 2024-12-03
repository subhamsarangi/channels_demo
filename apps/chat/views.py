from typing import List
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ninja import Router, NinjaAPI
from ninja.responses import Response

from .models import ChatRoom, ChatRoomMembership
from .mongo_models import Message
from apps.myauth.models import User

chat_api = NinjaAPI(urls_namespace="chat")
chat_router = Router()
chat_api.add_router("", chat_router)


@chat_router.get("")
@login_required
def chat_rooms(request):
    chat_room_list = ChatRoom.objects.all()
    return render(request, "chat/chat.html", {"rooms": chat_room_list})


@chat_router.post("")
@login_required
def create_chat_room(request):
    print(request.method, "00000000000000")
    name = request.POST.get("name")
    new_room = ChatRoom.objects.create(name=name)

    ChatRoomMembership.objects.create(chat_room=new_room, user=request.user)

    return redirect("chat:chat_room", slug=new_room.slug)


@chat_router.get("/{slug}")
@login_required
def chat_room(request, slug: str):
    chat_room = ChatRoom.objects.filter(slug=slug).first()

    if not chat_room:
        return render(request, "error.html", {"message": "Chat room not found"})

    return render(
        request,
        "chat/chat_room.html",
        {
            "name": chat_room.name,
            "slug": chat_room.slug,
        },
    )


@chat_router.get("/members/{slug}", response=List[str])
@login_required
def chat_room_members(request, slug: str):
    chat_room = ChatRoom.objects.filter(slug=slug).first()

    if not chat_room:
        # return Response({"error": "Chat room not found"}, status=404)
        return render(request, "error.html", {"message": "Chat room not found"})

    members = ChatRoomMembership.objects.filter(chat_room=chat_room).select_related(
        "user"
    )
    member_names = [member.user.full_name for member in members]

    return Response({"members": member_names})


@chat_router.get("/messages/{slug}", response=List[dict])
@login_required
def chat_room_messages(request, slug: str):
    chat_room = ChatRoom.objects.filter(slug=slug).first()

    if not chat_room:
        return render(request, "error.html", {"message": "Chat room not found"})

    messages = Message.objects.filter(chat_room=chat_room.id).order_by("created_at")

    formatted_messages = []
    for msg in messages:
        user = User.objects.get(id=msg.user)
        formatted_messages.append(
            {
                "user": user.full_name,
                "content": msg.content,
                "created_at": msg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "message_by_self": user == request.user,
            }
        )

    return Response({"messages": formatted_messages})
