from django.urls import path

from .views import BlogPostView , GetBlogsView

urlpatterns = [
    path('blog/' , BlogPostView.as_view()),
    path('blog/all/' , GetBlogsView.as_view()),
] 

