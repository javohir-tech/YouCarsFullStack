from django.shortcuts import render

# ================= REST FRAMEWORK ==================
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Max, Count

# ================== SERIAlIZER =====================
from .serializers import ChatHistorySerializer

# ============================ DB ===================
from .models import Message
from users.models import User

# ======================== PAGINATION ===============
from shared.custom_pagination import CustomPagination


class GetChathistory(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatHistorySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Message.objects.filter(
            Q(receiver_id=pk, sender=self.request.user)
            | Q(receiver=self.request.user, sender_id=pk)
        ).order_by("-created_time")


class ConversationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        me = self.request.user
        sent = (
            Message.objects.filter(sender=me)
            .values("receiver_id")
            .annotate(last_time=Max("created_time"))
        )
        receivered = (
            Message.objects.filter(receiver=me)
            .values("sender_id")
            .annotate(last_time=Max("created_time"))
        )

        partners_time = {}

        for row in sent:
            pid = row["receiver_id"]
            partners_time[pid] = max(
                partners_time.get(pid, row["last_time"]), row["last_time"]
            )
        for row in receivered:
            pid = row["sender_id"]
            partners_time[pid] = max(
                partners_time.get(pid, row["last_time"]), row["last_time"]
            )

        partners_time.pop(me.id, None)

        partners_ids = list(partners_time.keys())

        partners = {u.id: u for u in User.objects.filter(id__in=partners_ids)}

        last_messages = {}

        messages = Message.objects.filter(
            Q(receiver_id__in=partners_ids, sender=me)
            | Q(sender_id__in=partners_ids, receiver=me)
        ).order_by("-created_time")

        for msg in messages:
            pid = msg.receiver.id if msg.sender.id == me.id else msg.sender.id

            if pid not in last_messages:
                last_messages[pid] = msg

            if len(last_messages) == len(partners_ids):
                break
        unread_count = dict(
            Message.objects.filter(receiver=me, is_read=False)
            .values("sender_id")
            .annotate(c=Count("id"))
            .values_list("sender_id", "c")
        )

        conversations = []

        for pid, partner in partners.items():

            avatar = None
            message = last_messages.get(pid)
            
            if partner.photo and hasattr(partner.photo , "url"):
                if request is not None:
                    avatar = request.build_absolute_uri(partner.photo.url)
                else:
                    avatar = partner.photo.url
            
            conversations.append(
                {
                    "partner": partner.username,
                    "avatar" : avatar,
                    "partner_id": pid,
                    "last_message": message.content,
                    "is_read" : message.is_read,
                    "unread_count": unread_count.get(pid , 0),
                    "last_message_time": partners_time.get(pid, ""),
                    "last_sent_me": message.sender.id == me.id,
                    "is_new_partner": False,
                }
            )

        conversations.sort(key=lambda x: x["last_message_time"], reverse=True)

        return Response(conversations)
    



# Create your views here.
