from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from imr_grid_api.models import Post
from .serializers import PostSerializer


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
