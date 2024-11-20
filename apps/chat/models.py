from django.db import models
from apps.myauth.models import User


class ChatRoom(models.Model):
    """
    Model representing a chat room, which can be used for both individual
    and group chats. Each room is identified by a unique name, and timestamps
    are maintained for creation and updates.
    """

    name = models.CharField(max_length=255)
    is_group_chat = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ChatRoomMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "chat_room")

    def __str__(self):
        return f"{self.user.username} in {self.chat_room.name}"
