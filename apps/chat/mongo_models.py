import mongoengine as me


class Message(me.Document):
    """
    Model for a message sent to a GROUP CHAT or a DM"""

    user = me.IntField(required=True)
    chat_room = me.IntField(required=True)
    content = me.StringField(required=True)
    created_at = me.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.user} in {self.chat_room}"
