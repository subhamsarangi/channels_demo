from django.db import models
from django.conf import settings


class ChatRoom(models.Model):
    """Model for GROUP CHAT or a DM"""

    name = models.CharField(max_length=255)
    is_group_chat = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ChatRoomMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "chat_room")

    def __str__(self):
        return f"{self.user.full_name} in {self.chat_room.name}"
