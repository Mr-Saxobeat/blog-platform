from rest_framework import generics
from api import serializers
from django.contrib.auth.models import User
from api.models import Post, Comment, Category
from rest_framework import permissions
from rest_framework.renderers import TemplateHTMLRenderer
from api.permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class ListPosts(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/post/list_posts.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.data = {'posts': response.data}
        return response


class CreatePost(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/post/create_post.html'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        serializer = serializers.PostSerializer()
        return Response({'serializer': serializer})
    
    def post(self, request, *args, **kwargs):
        serializer = serializers.PostSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save(owner=request.user)
        # return Response({'serializer': serializer})
        return HttpResponseRedirect(redirect_to='/posts')


class DetailPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/post/detail_post.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.data = {'post': response.data}
        return response


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer