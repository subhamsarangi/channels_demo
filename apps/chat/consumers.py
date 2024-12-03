import json
from datetime import datetime

from ninja.responses import Response
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")
        if not self.user.is_authenticated:
            await self.close()
            return

        self.room_slug = self.scope["url_route"]["kwargs"]["room_slug"]
        self.room_group_name = f"chat_{self.room_slug}"
        self.chat_room = await self.get_chatroom(self.room_slug)

        await self.get_membership(self.user, self.chat_room)

        print("------> Connected::", self.room_group_name)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print("------> Disconnected::", self.room_group_name, close_code)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            content = data["content"]
            user_name = self.user.full_name
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            await self.save_message(self.user, self.chat_room, content)

            message_data = {
                "type": "chat_message",
                "content": content,
                "user": user_name,
                "user_id": self.user.id,
                "created_at": created_at,
            }

            print("------> Event Created::", self.room_group_name, message_data)
            await self.channel_layer.group_send(
                self.room_group_name,
                message_data,
            )
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error processing message: {e}")
            await self.send(text_data=json.dumps({"error": "Invalid message format"}))

    async def chat_message(self, event):
        content = event["content"]
        user = event["user"]
        user_id = event["user_id"]
        created_at = event["created_at"]

        if self.channel_name:
            message_payload = {
                "content": content,
                "user": user,
                "created_at": created_at,
                "message_by_self": self.user.id == user_id,
            }
            print("------> Event Sent::", self.room_group_name, message_payload)
            await self.send(text_data=json.dumps(message_payload))

    @database_sync_to_async
    def get_chatroom(self, room_slug):
        from .models import ChatRoom

        chat_room = ChatRoom.objects.filter(slug=room_slug).first()
        if not chat_room:
            return Response({"error": "Chat room not found"}, status=404)

        return chat_room

    @database_sync_to_async
    def get_membership(self, user, chat_room):
        # WILL HAVE TO BE UPDATED BECAUSE
        # MEMBERSHIPS NEEDS TO BE CREATED IN ADVANCE NOT JIT
        from .models import ChatRoomMembership

        membership, created = ChatRoomMembership.objects.get_or_create(
            user=user, chat_room=chat_room
        )
        return membership

    @database_sync_to_async
    def save_message(self, user, chat_room, content):
        from .mongo_models import Message

        message = Message.objects.create(
            user=user.id,
            chat_room=chat_room.id,
            content=content,
            created_at=datetime.now(),
        )
        return message
