from rest_framework import serializers
from .models import Message


class ChatHistorySerializer(serializers.ModelSerializer):

    sender = serializers.StringRelatedField()
    sender_id = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id",
            "content", 
            "sender",
            "sender_id",
            "created_time", 
            "updated_time",
            "is_read",
        ]

    def sender_id(self, obj):
        return str(obj.sender_id)
