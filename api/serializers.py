from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Post, Comment


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'posts',
            'comments',
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user



class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    status = serializers.CharField(style={'template': 'blog_ui/field_templates/not_render.html', 'hide_label': 'true'}, required=False)

    class Meta:
        model = Post
        fields = '__all__'