from django.shortcuts import redirect, render
from api import views
from api.serializers import PostSerializer, CommentSerializer
from django.views import View
from api.models import Post

class CreatePost(View):
    def get(self, request, *args, **kwargs):
        post_serializer = PostSerializer()
        return render(request, 'blog_ui/create_post.html', {'post_serializer': post_serializer})


    def post(self, request, *args, **kwargs):
        create_post_view = views.ListCreatePosts.as_view()
        data_response = create_post_view(request, format='json')
        data_json = data_response.render().data
        post_id = data_json['id']
        return redirect(f'/posts/{post_id}/')


def list_posts(request):
    list_post_view = views.ListCreatePosts.as_view()
    data_response = list_post_view(request, format='json')
    data_json = data_response.render().data
    context = {'posts': data_json}
    return render(request, 'blog_ui/list_posts.html', context)


def detail_post(request, pk):
    detail_post_view = views.DetailPost.as_view()
    data_response = detail_post_view(request, pk=pk, format='json')
    data_json = data_response.render().data
    new_comment_serializer = CommentSerializer()
    context = {
        'post': data_json,
        'new_comment': new_comment_serializer
        }
    return render(request, 'blog_ui/detail_post.html', context)


class EditPost(View):
    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        post_serializer = PostSerializer(post)
        return render(request, 'blog_ui/edit_post.html', {'post_serializer': post_serializer})


    def put(self, request, *args, **kwargs):
        create_post_view = views.DetailPost.as_view()
        data_response = create_post_view(request, pk=kwargs['pk'],format='json')
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
    data_response = create_comment_view(request, pk=pk, format='json')
    data_json = data_response.render().data
    post_id = data_json['id']
    return redirect(f'/posts/{post_id}/')