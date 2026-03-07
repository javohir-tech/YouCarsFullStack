import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Q
from .models import Message
from users.models import User


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

        updated = await self.update_message_read()

        if updated > 0:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "message_read",
                    "reader_id": str(self.me.id),
                    "reader": self.me.username,
                },
            )

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
                "id": str(msg.id),
                "content": msg.content,
                "sender": self.me.username,
                "sender_id": str(self.me.id),
                "created_time": msg.created_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "updated_time": msg.updated_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "is_read": msg.is_read,
            },
        )
        
        # await self.channel_layer.group_send(
        #     self.group_name,
        #     {
        #         "type": "message_read",
        #         "reader_id": str(self.me.id),
        #         "reader": self.me.username,
        #     },
        # )

        await self.channel_layer.group_send(
            f"conversations_{self.target_id}",
            {
                "type": "conversation_chat",
                "partner": self.me.username,
                "partner_id": str(self.me.id),
                "last_message": msg.content,
                "last_message_time": msg.created_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "last_sent_me": False,
                "is_read": msg.is_read,
            },
        )

        # await self.channel_layer.send()

        partner = await self.get_receiver()

        await self.channel_layer.group_send(
            f"conversations_{self.me.id}",
            {
                "type": "conversation_chat",
                "partner": partner.username,
                "partner_id": str(self.target_id),
                "last_message": msg.content,
                "last_message_time": msg.created_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "last_sent_me": True,
                "is_read": msg.is_read,
            },
        )

    async def message_read(self, event):
        await self.send(  
            text_data=json.dumps(
                {
                    "type": "message_read", 
                    "reader_id": event["reader_id"],
                    "reader": event["reader"],
                }
            )
        )

    async def chat_send(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "id": event["id"],
                    "content": event["content"],
                    "sender": event["sender"],
                    "sender_id": event["sender_id"],
                    "created_time": event["created_time"],
                    "updated_time": event["updated_time"],
                    "is_read": event["is_read"],
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

    @database_sync_to_async
    def update_message_read(self):
        return Message.objects.filter(
            receiver_id=self.me.id, sender_id=self.target_id, is_read=False
        ).update(is_read=True)

    @database_sync_to_async
    def get_receiver(self):
        return User.objects.get(id=self.target_id)


class ConversationsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.me = self.scope["user"]
        if self.me.is_anonymous:
            await self.close()
            return

        self.room_name = self.me.id
        self.group_name = f"conversations_{self.room_name}"
        self.partners_ids = await self.get_know_partners_ids()

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def conversation_chat(self, event):
        partner_id = event["partner_id"]

        is_new_partner = partner_id not in self.partners_ids

        if is_new_partner:
            self.partners_ids.add(partner_id)

        partner_avatar = await self.get_sender_avatar(partner_id)

        await self.send(
            text_data=json.dumps(
                {
                    "partner": event["partner"],
                    "partner_id": event["partner_id"],
                    "avatar": partner_avatar,
                    "last_message": event["last_message"],
                    "last_message_time": event["last_message_time"],
                    "last_sent_me": event["last_sent_me"],
                    "is_new_partner": is_new_partner,
                    "is_read": event["is_read"],
                }
            )
        )

    @database_sync_to_async
    def get_know_partners_ids(self):
        messages = Message.objects.filter(
            Q(sender=self.me) | Q(receiver=self.me)
        ).values_list("sender_id", "receiver_id")
        ids = set()

        for sender_id, receiver_id in messages:
            ids.add(str(sender_id))
            ids.add(str(receiver_id))

        ids.remove(str(self.me.id))

        return ids

    @database_sync_to_async
    def get_sender_avatar(self, id):
        user = User.objects.get(id=id)

        if user.photo:
            return user.photo.url

        return None
