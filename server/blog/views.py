from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Blog
from .serializers import BlogSerializer
from .permissions import BlogCreatePermissions


class BlogPostView(CreateAPIView):
    permission_classes = [IsAuthenticated, BlogCreatePermissions]
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Create your views here.
