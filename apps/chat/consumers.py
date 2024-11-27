import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")
        if not self.user.is_authenticated:
            await self.close()
            return

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.chat_room = await self.get_chatroom(self.room_name, True)

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
            message = data["message"]
            await self.save_message(self.user, self.chat_room, message)
            print(f"------> Data Received:: {self.room_group_name}, {data}")
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat_message", "message": message}
            )
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error processing message: {e}")
            await self.send(text_data=json.dumps({"error": "Invalid message format"}))

    async def chat_message(self, event):
        message = event["message"]
        if self.channel_name:
            print("------> Event Sent::", self.room_group_name, message)
            await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def get_chatroom(self, room_name, is_group_chat):
        from .models import ChatRoom

        chat_room, created = ChatRoom.objects.get_or_create(
            name=room_name, is_group_chat=is_group_chat
        )
        return chat_room

    @database_sync_to_async
    def get_membership(self, user, chat_room):
        from .models import ChatRoomMembership

        membership, created = ChatRoomMembership.objects.get_or_create(
            user=user, chat_room=chat_room
        )
        return membership

    @database_sync_to_async
    def save_message(self, user, chat_room, content):
        from .mongo_models import Message

        message = Message.objects.create(
            user=user.id, chat_room=chat_room.id, content=content
        )
        return message
