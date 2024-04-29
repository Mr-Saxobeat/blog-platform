from django.test import TestCase
from unittest.mock import patch, Mock, MagicMock
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsOwnerOrReadOnly
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
    @patch('api.views.super')
    def test_put_published(self, mock_super):
        # Given
        data_dict = {'status': 'published'}
        mock_data = MagicMock()
        mock_data.__getitem__.side_effect = data_dict.__getitem__
        mock_data.pop = Mock()

        mock_request = Mock(data=mock_data)

        mock_view = Mock(spec=DetailPost)
        mock_view.request = mock_request
        mock_view.get_object = Mock(return_value=Mock(status='published'))
        mock_view.put = DetailPost.put

        mock_super().put = Mock()

        # When
        mock_view.put(mock_view, mock_request)

        # Then
        mock_data.pop.assert_called_once_with('status')
        mock_super().put.assert_called_once_with(mock_request)

    @patch('api.views.super')
    def test_put_draft(self, mock_super):
        # Given
        data_dict = {'status': 'draft'}
        mock_data = MagicMock()
        mock_data.__getitem__.side_effect = data_dict.__getitem__
        mock_data.pop = Mock()

        mock_request = Mock(data=mock_data)

        mock_view = Mock(spec=DetailPost)
        mock_view.request = mock_request
        mock_view.get_object = Mock(return_value=Mock(status='draft'))
        mock_view.put = DetailPost.put

        mock_super().put = Mock()

        # When
        mock_view.put(mock_view, mock_request)

        # Then
        mock_data.pop.assert_not_called()
        mock_super().put.assert_called_once_with(mock_request)


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