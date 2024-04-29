from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveAPIView
)
from api import serializers
from django.contrib.auth.models import User
from api.models import Post, Comment
from rest_framework import permissions
from api.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from api.serializers import PostSerializer, CommentSerializer, UserSerializer


class ListCreatePosts(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DetailPost(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    
    def put(self, request, *args, **kwargs):
        post = self.get_object()
        post_serializer = PostSerializer(post, data=request.data)
        post_serializer.title = request.data.get('title', post.title)
        post_serializer.body = request.data.get('body', post.body)

        if request.data.get('status') != 'published':
            post_serializer.status = request.data.get('status', post.status)

        if post_serializer.is_valid():
            post_serializer.save()

        return Response(post_serializer.data)


class ListCreateComments(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DetailComment(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class ListCreateUsers(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DetailUser(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer