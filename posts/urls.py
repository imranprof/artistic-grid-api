from django.urls import path
from .views import PostCreateView
from .views import PostListView
from .views import PostDetailView

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),         # GET all posts
    path("create/", PostCreateView.as_view(), name="post-create"),  # POST new post
    path("<int:id>/", PostDetailView.as_view(), name="post-detail"), # GET one post

]
