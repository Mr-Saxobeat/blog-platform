from django.test import TestCase
from unittest.mock import patch, Mock, MagicMock
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsOwnerOrReadOnly
from api.serializers import PostSerializer, UserSerializer
from api.views import (
    DetailComment, DetailUser, ListCreateComments, ListCreatePosts,
    DetailPost, ListCreateUsers
    )
from parameterized import parameterized

class TestListCreatePostsView(TestCase):
    def test_view_properties(self):
        # Given
        view = ListCreatePosts()

        # Then
        self.assertEqual(view.queryset.model.__name__, 'Post')
        self.assertEqual(view.serializer_class.__name__, 'PostSerializer')
        self.assertEqual(view.permission_classes, [IsAuthenticatedOrReadOnly])
        self.assertEqual(view.filter_backends, [DjangoFilterBackend])
        self.assertEqual(view.filterset_fields, '__all__')


    def test_perform_create(self):
        # Given
        mock_request = Mock(user='mock_user')
        view = ListCreatePosts()
        view.request = mock_request
        mock_serializer = Mock()
        mock_serializer.save = Mock()

        # When
        view.perform_create(mock_serializer)

        # Then
        mock_serializer.save.assert_called_once_with(owner=mock_request.user)

class TestDetailPostView(TestCase):
    def test_view_properties(self):
        # Given
        view = DetailPost()

        # Then
        self.assertEqual(view.queryset.model.__name__, 'Post')
        self.assertEqual(view.serializer_class.__name__, 'PostSerializer')
        self.assertEqual(view.permission_classes, [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly])


    @parameterized.expand([
        ['published', 'published', True],
        ['published', 'published', False],
        ['published', 'draft', True],
        ['published', 'draft', False],
        ['draft', 'published', True],
        ['draft', 'published', False],
        ['draft', 'draft', True],
        ['draft', 'draft', False],
    ])
    @patch('api.views.PostSerializer')
    def test_put(self, data_status, object_status, is_valid_return, mock_serializer):
        # Given
        mock_is_valid = Mock(return_value=is_valid_return)
        mock_serializer.is_valid = mock_is_valid

        mock_save = Mock()
        mock_serializer.save = mock_save

        mock_serializer = Mock(is_valid=mock_is_valid, save=mock_save)
        mock_serializer_class = Mock(return_value=mock_serializer)

        view = Mock()
        view.serializer_class = mock_serializer_class
        view.put = DetailPost.put

        mock_post_object = Mock(
            title='mock_title',
            body='mock_body',
            status=object_status
        )
        view.get_object = Mock(return_value=mock_post_object)

        data_dict = {
            'title': 'mock_title_modified',
            'body': 'mock_body_modified',
            'status': data_status
        }
        mock_data = MagicMock()
        mock_data.__getitem__.side_effect = data_dict.__getitem__
        mock_data.get = Mock()
        mock_request = Mock(data=mock_data)

        # When
        view.put(view, mock_request)

        # Then
        if is_valid_return == True:
            mock_save.assert_called_once()
        else:
            mock_save.assert_not_called()
        
        if data_status != 'published':
            mock_data.get.assert_called_with('status', object_status)


class TestListCreateCommentsView(TestCase):
    def test_view_properties(self):
        # Given
        view = ListCreateComments()

        # Then
        self.assertEqual(view.queryset.model.__name__, 'Comment')
        self.assertEqual(view.serializer_class.__name__, 'CommentSerializer')
        self.assertEqual(view.permission_classes, [IsAuthenticatedOrReadOnly])


    def test_perform_create(self):
        # Given
        mock_request = Mock(user='mock_user')
        view = ListCreateComments()
        view.request = mock_request
        mock_serializer = Mock()
        mock_serializer.save = Mock()

        # When
        view.perform_create(mock_serializer)

        # Then
        mock_serializer.save.assert_called_once_with(owner=mock_request.user)

class TestDetailCommentView(TestCase):
    def test_view_properties(self):
        # Given
        view = DetailComment()

        # Then
        self.assertEqual(view.queryset.model.__name__, 'Comment')
        self.assertEqual(view.serializer_class.__name__, 'CommentSerializer')
        self.assertEqual(view.permission_classes, [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly])


class TestDetailUserView(TestCase):
    def test_view_properties(self):
        # Given
        view = DetailUser()

        # Then
        self.assertEqual(view.queryset.model.__name__, 'User')
        self.assertEqual(view.serializer_class.__name__, 'UserSerializer')


class TestListCreateUsersView(TestCase):
    def test_view_properties(self):
        # Given
        view = ListCreateUsers()

        # Then
        self.assertEqual(view.queryset.model.__name__, 'User')
        self.assertEqual(view.serializer_class.__name__, 'UserSerializer')


class TestPermissions(TestCase):
    @parameterized.expand([
        ('GET', 'same_owner', 'same_owner', True),
        ('GET', 'different_owner', 'another_owner', True),

        ('HEAD', 'same_owner', 'same_owner', True),
        ('HEAD', 'different_owner', 'another_owner', True),
        
        ('OPTIONS', 'same_owner', 'same_owner', True),
        ('OPTIONS', 'different_owner', 'another_owner', True),

        ('POST', 'same_owner', 'same_owner', True),
        ('POST', 'different_owner', 'another_owner', False),

        ('PUT', 'same_owner', 'same_owner', True),
        ('PUT', 'different_owner', 'another_owner', False),

        ('PATCH', 'same_owner', 'same_owner', True),
        ('PATCH', 'different_owner', 'another_owner', False),

        ('DELETE', 'same_owner', 'same_owner', True),
        ('DELETE', 'different_owner', 'another_owner', False),
    ])
    def test_IsOwnerOrReadOnly(self, method, obj_owner, request_user, expected):
        # Given
        permission = IsOwnerOrReadOnly()

        mock_request = Mock(user=request_user, method=method)
        mock_obj = Mock(owner=obj_owner)
        mock_view = Mock()

        # When
        result = permission.has_object_permission(mock_request, mock_view, mock_obj)

        # Then
        self.assertEqual(result, expected)


class TestUserSerializer(TestCase):
    @patch('api.serializers.User.objects')
    def test_create(self, mock_user_objects):
        # Given
        serializer = UserSerializer()
        mock_validated_data = {
            'username': 'test_username',
            'password': 'test_password'
        }
        mock_user_objects.create_user = Mock(return_value=mock_validated_data)

        # When
        result = serializer.create(mock_validated_data)

        # Then
        mock_user_objects.create_user.assert_called_once_with(
            username=mock_validated_data['username'],
            password=mock_validated_data['password']
        )
        self.assertEqual(result, mock_validated_data)

