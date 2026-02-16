from django.urls import path

from .views import BlogPostView, GetBlogsView, DetailBlogView, SemialerBlogsView

urlpatterns = [
    path("blog/", BlogPostView.as_view()),
    path("blog/all/", GetBlogsView.as_view()),
    path("blog/detail/<uuid:pk>/", DetailBlogView.as_view()),
    path("blog/semiler/<uuid:pk>/", SemialerBlogsView.as_view()),
]
