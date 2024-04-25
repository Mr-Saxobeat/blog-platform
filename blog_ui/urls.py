from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth.decorators import login_required
from django.urls import path
from blog_ui import views

urlpatterns = [
    path('', views.list_posts),
    path('posts/new/', login_required(views.CreatePost.as_view(), login_url='/api-auth/login/?next=/')),
    path('posts/<int:pk>/', views.detail_post),
    path('posts/<int:pk>/edit/', login_required(views.EditPost.as_view(), login_url='/api-auth/login/?next=/')),
    path('posts/<int:pk>/delete/', login_required(views.delete_post, login_url='/api-auth/login/?next=/')),
    path('posts/<int:pk>/comments/', login_required(views.create_comment, login_url='/api-auth/login/?next=/')),
]


urlpatterns = format_suffix_patterns(urlpatterns)