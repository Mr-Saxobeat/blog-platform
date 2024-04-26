from django.shortcuts import redirect, render
from api import views
from api.serializers import PostSerializer, CommentSerializer
from django.views import View
from api.models import Post
from django.contrib.auth.forms import UserCreationForm

class CreatePost(View):
    def get(self, request, *args, **kwargs):
        post_serializer = PostSerializer()
        context = {
            'page_title': 'New Post',
            'post_serializer': post_serializer
            }
        return render(request, 'blog_ui/create_post.html', context)


    def post(self, request, *args, **kwargs):
        create_post_view = views.ListCreatePosts.as_view()
        data_response = create_post_view(request, format='json')
        data_json = data_response.render().data
        post_id = data_json['id']
        return redirect(f'/posts/{post_id}/')


def list_posts(request):
    request_get = request.GET.copy()
    request_get['status'] = 'published'
    request.GET = request_get
    list_post_view = views.ListCreatePosts.as_view()
    data_response = list_post_view(request, format='json')
    data_json = data_response.render().data
    context = {
        'page_title': 'Posts',
        'posts': data_json
        }
    return render(request, 'blog_ui/list_posts.html', context)

def list_drafts_posts(request):
    request_get = request.GET.copy()
    request_get['status'] = 'draft'
    request.GET = request_get
    list_drafts_posts_view = views.ListCreatePosts.as_view()
    data_response = list_drafts_posts_view(request, format='json')
    data_json = data_response.render().data
    context = {
        'page_title': 'Draft Posts',
        'posts': data_json
        }
    return render(request, 'blog_ui/list_posts.html', context)


def detail_post(request, pk):
    detail_post_view = views.DetailPost.as_view()
    data_response = detail_post_view(request, pk=pk, format='json')
    data_json = data_response.render().data
    new_comment_serializer = CommentSerializer()
    context = {
        'page_title': '',
        'post': data_json,
        'new_comment': new_comment_serializer
        }
    return render(request, 'blog_ui/detail_post.html', context)


class EditPost(View):
    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        post_serializer = PostSerializer(post)
        context = {
            'page_title': 'Edit Post',
            'post_serializer': post_serializer
            }
        return render(request, 'blog_ui/edit_post.html', context)


    def post(self, request, *args, **kwargs):
        request.method = 'PUT'
        create_post_view = views.DetailPost.as_view()
        data_response = create_post_view(request, pk=kwargs['pk'], format='json')
        data_json = data_response.render().data
        post_id = data_json['id']
        return redirect(f'/posts/{post_id}/')


def delete_post(request, pk):
    delete_post_view = views.DetailPost.as_view()
    request.method = 'DELETE'
    delete_post_view(request, pk=pk, format='json')
    return redirect('/')


def create_comment(request, pk):
    create_comment_view = views.ListCreateComments.as_view()
    create_comment_view(request, format='json')
    post_id = pk
    return redirect(f'/posts/{post_id}/')


class CreateUser(View):
    def get(self, request, *args, **kwargs):
        user_creation_form = UserCreationForm()  
        context = {
            'page_title': 'New User',
            'user_creation_form': user_creation_form,
        }
        return render(request, 'blog_ui/create_user.html', context)


    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)  
        if form.is_valid():  
            form.save() 
        return redirect('/api-auth/login/?next=/')