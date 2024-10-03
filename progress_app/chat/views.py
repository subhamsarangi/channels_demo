from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from myauth.models import User
from .models import ChatRoom, ChatRoomMembership
from .mongo_models import Message


@login_required
def create_group(request):
    if request.method == "POST":
        name = request.POST.get("name")
        is_group_chat = request.POST.get("is_group_chat", "false") == "true"
        chat_room = ChatRoom.objects.create(name=name, is_group_chat=is_group_chat)
        ChatRoomMembership.objects.create(user=request.user, chat_room=chat_room)
        return JsonResponse(
            {"message": "Group created successfully", "group_id": chat_room.id},
            status=201,
        )


@login_required
def add_member_to_group(request, group_id):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        chat_room = get_object_or_404(ChatRoom, id=group_id)
        user = get_object_or_404(User, id=user_id)
        membership, created = ChatRoomMembership.objects.get_or_create(
            user=user, chat_room=chat_room
        )
        return JsonResponse(
            {"message": "Member added successfully", "created": created}, status=201
        )


@login_required
def list_groups(request):
    chat_rooms = ChatRoom.objects.all()
    group_list = [
        {"id": room.id, "name": room.name, "is_group_chat": room.is_group_chat}
        for room in chat_rooms
    ]
    return JsonResponse(group_list, safe=False)


@login_required
def send_message_to_group(request, group_id):
    if request.method == "POST":
        content = request.POST.get("content")
        chat_room = get_object_or_404(ChatRoom, id=group_id)
        message = Message(user=request.user, chat_room=chat_room, content=content)
        message.save()
        return JsonResponse(
            {"message": "Message sent successfully", "message_id": str(message.id)},
            status=201,
        )
