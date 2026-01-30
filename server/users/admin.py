from django.contrib import admin
from .models import User, UserConfirmation

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ["id", "username", "email", "is_staff"]
    search_fields = ["username", "email"]

@admin.register(UserConfirmation)  
class UserConfirmationAdmin(admin.ModelAdmin):
    list_display = ["id" , "code" , "user"]


# Register your models here.
