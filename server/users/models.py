from django.db import models

# //////////// BaseModel ///////////
from shared.models import BaseModel

# ////// user model //////////
from django.contrib.auth.models import AbstractUser


class USER_ROLE(models.TextChoices):
    ORDENARY_USER = "ordenary_user", "Ordenary User"
    MANAGER = "manager", "Manager"
    OPERATOR = "operator", "Operator"


class User(BaseModel, AbstractUser):

    user_role = models.CharField(
        max_length=13, choices=USER_ROLE.choices, default=USER_ROLE.ORDENARY_USER
    )
    
    def token(self) :
        pass
    


# Create your models here.
