import mongoengine as me


class User(me.Document):
    username = me.StringField(required=True)


class ChatRoom(me.Document):
    name = me.StringField(required=True)


class Message(me.Document):
    """
    Model for a message sent to a GROUP CHAT or a DM"""

    user = me.ReferenceField(User, required=True)
    chat_room = me.ReferenceField(ChatRoom, required=True)
    content = me.StringField(required=True)
    created_at = me.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.user.username} in {self.chat_room.name if self.chat_room else 'Direct Message'}"
