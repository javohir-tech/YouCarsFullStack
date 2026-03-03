from django.shortcuts import render

# ================= REST FRAMEWORK ==================
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

# ================== SERIAlIZER =====================
from .serializers import ChatHistorySerializer

# ============================ DB ===================
from .models import Message

# ======================== PAGINATION ===============
from shared.custom_pagination import CustomPagination


class GetChathistory(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatHistorySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Message.objects.filter(
            Q(receiver_id=pk, sender=self.request.user)
            | Q(receiver=self.request.user, sender_id=pk)
        ).order_by("-created_time")


# Create your views here.
