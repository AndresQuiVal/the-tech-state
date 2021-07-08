from django.shortcuts import render
from django.views import generic
from .models import Post

def index_view(request): # TODO: transform to generic ListView class
    """
    Returns the main template in the app
    """
    posts = Post.objects.all()
    context = {
        'post_list' : posts
    }

    return render(request, 'blog/index.html', context)


class PostList(generic.ListView):
    template_name = 'blog/index.html'
    queryset = Post.objects.all()

class PostDetail(generic.DetailView):
    model = Post

