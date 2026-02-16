from django.db import models
from shared.models import BaseModel
from users.models import User
from django.core.validators import FileExtensionValidator


class Blog(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    title = models.CharField(max_length=250)
    text = models.TextField()
    image = models.ImageField(
        upload_to="blog",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "heic", "heif"]
            ),
        ],
    )

    def __str__(self):
        return f"{self.title}"


# Create your models here.
