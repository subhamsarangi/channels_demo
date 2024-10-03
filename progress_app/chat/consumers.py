import json
from channels.generic.websocket import AsyncWebsocketConsumer

from .mongo_models import Message


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.chat_room_group_name = f"chat_{self.chat_room_id}"

        await self.channel_layer.group_add(self.chat_room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json["content"]
        user = self.scope["user"]

        message = Message(user=user, chat_room=self.chat_room_id, content=content)
        message.save()

        await self.channel_layer.group_send(
            self.chat_room_group_name,
            {"type": "chat_message", "message": content, "user": str(user.username)},
        )

    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]

        await self.send(text_data=json.dumps({"message": message, "user": user}))
