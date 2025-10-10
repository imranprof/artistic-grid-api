from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from imr_grid_api.models import Post
from .serializers import PostSerializer


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


#for all public post retrive
class PostListView(generics.ListAPIView):
    queryset = Post.objects.filter(status="published").order_by("-created_at")
    serializer_class = PostSerializer


# for get single post
class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.filter(status="published")
    serializer_class = PostSerializer
    lookup_field = "id"  
