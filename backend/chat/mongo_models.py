import mongoengine as me


class Message(me.Document):
    """
    Model representing a message sent by a user in a chat room or as a direct message.
    Each message contains content, the user who sent it, and a reference
    to the chat room where it was sent.
    """

    user = me.ReferenceField("myauth.User", required=True)
    chat_room = me.ReferenceField("ChatRoom")
    content = me.StringField(required=True)
    created_at = me.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.user.username} in {self.chat_room.name if self.chat_room else 'Direct Message'}"
