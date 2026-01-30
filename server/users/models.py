import random
from datetime import timedelta
from django.db import models
from django.utils import timezone


# //////////// BaseModel ///////////P
from shared.models import BaseModel

# ////// user model //////////
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


class USER_ROLE(models.TextChoices):
    ORDENARY_USER = "ordenary_user", "Ordenary User"
    MANAGER = "manager", "Manager"
    OPERATOR = "operator", "Operator"


class Auth_STATUS(models.TextChoices):
    REGISTER = "register", "Register"
    VERIFY_CODE = "verify_code", "Verify Code"
    EDIT_PASSWORD = "edit_password", "Edit password"
    DONE = "done", "Done"


class User(BaseModel, AbstractUser):

    user_role = models.CharField(
        max_length=13, choices=USER_ROLE.choices, default=USER_ROLE.ORDENARY_USER
    )
    email = models.EmailField(max_length=128, unique=True)
    auth_status = models.CharField(
        choices=Auth_STATUS.choices, default=Auth_STATUS.REGISTER
    )
    photo = models.ImageField(upload_to="user/profile", blank=True, null=True)

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {"access_token": str(refresh.access_token), "refresh": str(refresh)}

    def create_confirmation(self):
        code = "".join([str(random.randint(1, 10000) % 10) for _ in range(4)])
        UserConfirmation.objects.create(
            code=code, user=self, expire_time=timezone.now() + timedelta(minutes=2)
        )

        return code

    def check_email(self):
        if self.email:
            current_email = self.email.lower().strip()
            self.email = current_email

    def __str__(self):
        return f"{self.username}"

    def save(self, *args, **kwargs):
        self.check_email()
        super().save(*args, **kwargs)


class UserConfirmation(BaseModel):
    code = models.CharField(max_length=4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verify")
    expire_time = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    def __str__(self):
        return f"{self.user.__str__()} ni code"


# Create your models here.
