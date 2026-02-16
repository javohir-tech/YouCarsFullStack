from django.contrib import admin
from .models import Blog


@admin.register(Blog)
class adminBlog(admin.ModelAdmin):
    list_display = ["image", "title", "text", "author"]


# Register your models here.
