from typing import List
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
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


## messages admininstration


@chat_router.get("/management/messages")
@login_required
def message_management(request):
    if request.user.is_admin == False:
        return render(request, "error.html", {"message": "You cannot see this page"})

    messages = Message.objects.filter(user=request.user.id).order_by("-created_at")
    formatted_messages = []
    for msg in messages:
        user = User.objects.get(id=msg.user)
        formatted_messages.append(
            {
                "id": msg.id,
                "user": user.full_name,
                "content": msg.content,
                "created_at": msg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    paginator = Paginator(formatted_messages, 5)
    page_number = request.GET.get("page", 1)
    page = paginator.get_page(page_number)

    return render(
        request,
        "chat/message_management.html",
        {
            "chatmessages": page.object_list,
            "page": page,
        },
    )


@chat_router.get("/management/message/{message_id}/edit")
@login_required
def edit_message(request, message_id: str):
    if request.user.is_admin == False:
        return render(request, "error.html", {"message": "You cannot see this page"})

    message = Message.objects.filter(id=message_id).first()

    if not message:
        raise Http404("Message not found")

    return render(request, "chat/edit_message.html", {"message": message})


@chat_router.post("/management/message/{message_id}/edit")
@login_required
def update_message(request, message_id: str):
    if request.user.is_admin == False:
        return render(request, "error.html", {"message": "You cannot see this page"})

    message = Message.objects.filter(id=message_id).first()

    if not message:
        raise Http404("Message not found")

    new_content = request.POST.get("content")
    message.content = new_content
    message.save()

    return redirect("chat:message_management")


@chat_router.get("/management/message/{message_id}/delete")
@login_required
def confirm_delete_message(request, message_id: str):
    if request.user.is_admin == False:
        return render(request, "error.html", {"message": "You cannot see this page"})

    message = Message.objects.filter(id=message_id).first()

    if not message:
        raise Http404("Message not found")

    return render(request, "chat/confirm_delete_message.html", {"message": message})


@chat_router.post("/management/message/{message_id}/delete")
@login_required
def delete_message(request, message_id: str):
    if request.user.is_admin == False:
        return render(request, "error.html", {"message": "You cannot see this page"})

    message = Message.objects.filter(id=message_id).first()

    if not message:
        raise Http404("Message not found")

    message.delete()
    return redirect("chat:message_management")
