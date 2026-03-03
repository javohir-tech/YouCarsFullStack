from django.db import models
from shared.models import BaseModel
from users.models import User


class Message(BaseModel):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_message"
    )
    reveiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receive_message"
    )
    content = models.TextField(max_length=1200)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_time"]
        
    def __str__(self):
        return f"{self.sender}->{self.reveiver} : {self.content[:30]}"
    


# Create your models here.
