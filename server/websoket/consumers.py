import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Q
from .models import Message
from users.models import User
from django.core.cache import cache
from django.conf import settings

ONLINE_KEY = "user_online_{user_id}"
ONLINE_TIMEOUT = 86400


async def set_user_online(user_id: str, is_online: bool):
    key = ONLINE_KEY.format(user_id=user_id)
    if is_online:
        await asyncio.to_thread(cache.set, key, True, timeout=ONLINE_TIMEOUT)
    else:
        await asyncio.to_thread(cache.delete, key)


async def is_user_online(user_id: str) -> bool:
    key = ONLINE_KEY.format(user_id=user_id)
    result = await asyncio.to_thread(cache.get, key)
    return result is True


class PresenceConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.me = self.scope["user"]
        if self.me.is_anonymous:
            await self.close()
            return

        self.user_id = str(self.me.id)
        self.group_name = f"presence_{self.user_id}"

        await set_user_online(self.user_id, True)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        partner_ids = await self.get_partners_ids()
        for pid in partner_ids:
            await self.channel_layer.group_send(
                f"presence_watch_{pid}",
                {
                    "type": "partner_online",
                    "user_id": self.user_id,
                    "is_online": True,
                },
            )

    async def disconnect(self, code):
        await set_user_online(self.user_id, False)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

        partner_ids = await self.get_partners_ids()

        for pid in partner_ids:
            await self.channel_layer.group_send(
                f"presence_watch_{pid}",
                {
                    "type": "partner_online",
                    "user_id": self.user_id,
                    "is_online": False,
                },
            )

    @database_sync_to_async
    def get_partners_ids(self):
        messages = Message.objects.filter(
            Q(sender_id=self.user_id) | Q(receiver_id=self.user_id)
        ).values_list("sender_id", "receiver_id")

        ids = set()

        for sender_id, receiver_id in messages:
            ids.add(str(sender_id))
            ids.add(str(receiver_id))

        ids.discard(str(self.user_id))

        return ids


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.me = self.scope["user"]
        self.target_id = self.scope["url_route"]["kwargs"]["user_id"]

        if self.me.is_anonymous:
            await self.close()
            return

        self.room_name = self.get_room_name(self.me.id, self.target_id)
        self.group_name = f"chat_{self.room_name}"

        self.watch_group = f"presence_watch_{self.me.id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.channel_layer.group_add(self.watch_group, self.channel_name)
        await self.set_user_in_room(True)
        await self.accept()

        target_online = await is_user_online(str(self.target_id))
        await self.send(
            text_data=json.dumps(
                {
                    "type": "partner_online",
                    "user_id": str(self.target_id),
                    "is_online": target_online,
                }
            )
        )

        updated = await self.update_message_read()

        if updated > 0:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "message_read",
                    "reader_id": str(self.target_id),
                },
            )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.watch_group, self.channel_name)
        await self.set_user_in_room(False)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        content = data.get("message", "")

        target_online = await self.is_terget_in_room()

        if target_online:
            msg = await self.save_message(content, True)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "message_read",
                    "reader_id": str(self.target_id),
                },
            )
        else:
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

    # ---- Event handlers ----

    async def message_read(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "message_read",
                    "reader_id": event["reader_id"],
                }
            )
        )

    async def partner_online(self, event):
        if event["user_id"] == str(self.target_id):
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "partner_online",
                        "user_id": event["user_id"],
                        "is_online": event["is_online"],
                    }
                )
            )

    async def chat_send(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type" : "chat_send",
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

    # ---- Helpers ----

    async def set_user_in_room(self, is_present: bool):
        key = f"room_presence_{self.room_name}_{self.me.id}"
        if is_present:
            await asyncio.to_thread(cache.set, key, True, timeout=86400)
        else:
            await asyncio.to_thread(cache.delete, key)

    async def is_terget_in_room(self) -> bool:
        key = f"room_presence_{self.room_name}_{self.target_id}"
        result = await asyncio.to_thread(cache.get, key)
        return result is True

    @staticmethod
    def get_room_name(user_id, target_id):
        ids = sorted([str(user_id), str(target_id)])
        return f"{ids[0]}_{ids[1]}"

    @database_sync_to_async
    def save_message(self, content, is_read: bool = False):
        message = Message.objects.create(
            sender_id=self.me.id,
            receiver_id=self.target_id,
            content=content,
            is_read=is_read,
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


# ============================================================
# CONVERSATIONS CONSUMER
# ============================================================
class ConversationsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.me = self.scope["user"]
        if self.me.is_anonymous:
            await self.close()
            return

        self.room_name = self.me.id
        self.group_name = f"conversations_{self.room_name}"
        self.partners_ids = await self.get_know_partners_ids()

        self.watch_group = f"presence_watch_{self.me.id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.channel_layer.group_add(self.watch_group, self.channel_name)
        await self.accept()

        online_statuses = {}
        for pid in self.partners_ids:
            online_statuses[pid] = await is_user_online(pid)

        await self.send(
            text_data=json.dumps(
                {"type": "online_statuses", "statuses": online_statuses}
            )
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.watch_group , self.channel_name)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def partner_online(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "partner_online",
                    "user_id": event["user_id"],
                    "is_online": event["is_online"],
                }
            )
        )

    async def conversation_chat(self, event):
        partner_id = event["partner_id"]

        is_new_partner = partner_id not in self.partners_ids

        if is_new_partner:
            self.partners_ids.add(partner_id)

        partner_avatar = await self.get_sender_avatar(partner_id)

        await self.send(
            text_data=json.dumps(
                {
                    "type" : "conversation",
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

        ids.discard(str(self.me.id))

        return ids

    @database_sync_to_async
    def get_sender_avatar(self, id):
        user = User.objects.get(id=id)
        
        base_url = settings.BASE_URL

        if user.photo:
            return f"{base_url}{user.photo.url}"

        return None
