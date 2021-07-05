from django.shortcuts import render
from .models import Post

def index_view(request):
    """
    Returns the main template in the app
    """
    posts = Post.objects.all()
    context = {
        'posts' : posts
    }

    return render(request, 'blog/index.html', context)

