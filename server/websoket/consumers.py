import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Q
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.me = self.scope["user"]
        self.target_id = self.scope["url_route"]["kwargs"]["user_id"]

        if self.me.is_anonymous:
            await self.close()
            return

        self.room_name = self.get_room_name(self.me.id, self.target_id)
        self.group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        content = data.get("message", "")

        msg = await self.save_message(content)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_send",
                "message": msg.content,
                "receiver": self.me.username,
                "receiver_id": str(self.me.id),
                "created_time": msg.created_time.strftime("%H:%M"),
            },
        )

    async def chat_send(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "receiver": event["receiver"],
                    "receiver_id": event["receiver_id"],
                    "created_time": event["created_time"],
                }
            )
        )

    @staticmethod
    def get_room_name(user_id, target_id):
        ids = sorted([str(user_id), str(target_id)])
        return f"{ids[0]}_{ids[1]}"

    @database_sync_to_async
    def save_message(self, content):
        message = Message.objects.create(
            sender_id=self.me.id, receiver_id=self.target_id, content=content
        )

        return message
