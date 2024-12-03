import random
import string

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver


class ChatRoom(models.Model):
    """Model for GROUP CHAT or a DM"""

    name = models.CharField(max_length=255)
    is_group_chat = models.BooleanField(default=False)
    slug = models.SlugField(blank=True, editable=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def generate_slug(self):
        random_string = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=10)
        )
        return f"{slugify(self.name)}-{random_string}"


@receiver(pre_save, sender=ChatRoom)
def create_chat_room_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = instance.generate_slug()


class ChatRoomMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "chat_room")

    def __str__(self):
        return f"{self.user.full_name} in {self.chat_room.name}"
