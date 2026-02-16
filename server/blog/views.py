from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView , RetrieveAPIView 
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Blog
from .serializers import BlogSerializer
from .permissions import BlogCreatePermissions
from shared.custom_pagination import CustomPagination

class BlogPostView(CreateAPIView):
    permission_classes = [IsAuthenticated, BlogCreatePermissions]
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GetBlogsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BlogSerializer
    queryset = Blog.objects.all().order_by("-created_time")
    pagination_class = CustomPagination
    
class DetailBlogView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    
class SemialerBlogsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BlogSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        blog_id = self.kwargs.get("pk")
        return Blog.objects.exclude(id = blog_id)
    
    
    
    


# Create your views here.
