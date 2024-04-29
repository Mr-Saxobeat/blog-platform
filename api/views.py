from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveAPIView
)
from api import serializers
from django.contrib.auth.models import User
from api.models import Post, Comment
from rest_framework import permissions
from api.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class ListCreatePosts(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DetailPost(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    
    def put(self, request, *args, **kwargs):
        post = self.get_object()
        if post.status == 'published':
            request.data.pop('status')
        return super().put(request, *args, **kwargs)


class ListCreateComments(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DetailComment(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class ListCreateUsers(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class DetailUser(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer