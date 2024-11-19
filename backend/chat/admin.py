from django.contrib import admin

from .models import ChatRoom, ChatRoomMembership

admin.site.register(ChatRoom)

admin.site.register(ChatRoomMembership)
