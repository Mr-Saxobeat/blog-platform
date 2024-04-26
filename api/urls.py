from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from api import views

urlpatterns = [
    path('users/', views.ListCreateUsers.as_view()),
    path('users/<int:pk>/', views.DetailUser.as_view()),
    path('posts/', views.ListCreatePosts.as_view()),
    path('posts/<int:pk>/', views.DetailPost.as_view()),
    path('comments/', views.ListCreateComments.as_view()),
    path('comments/<int:pk>/', views.DetailComment.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)