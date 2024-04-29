from django.test import TestCase
from unittest.mock import patch, Mock, MagicMock
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from api.views import ListCreatePosts, DetailPost

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


class TestListCreateComments(TestCase):
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

class TestDetailComment(TestCase):
    def test_view_properties(self):
        # Given
        view = DetailComment()

        # Then
        self.assertEqual(view.queryset.model.__name__, 'Comment')
        self.assertEqual(view.serializer_class.__name__, 'CommentSerializer')
        self.assertEqual(view.permission_classes, [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly])


class TestDetailUser(TestCase):
    def test_view_properties(self):
        # Given
        view = DetailUser()

        # Then
        self.assertEqual(view.queryset.model.__name__, 'User')
        self.assertEqual(view.serializer_class.__name__, 'UserSerializer')
