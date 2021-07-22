from django.shortcuts import render
from django.views import generic
from .models import Post

class PostList(generic.ListView):
    template_name = 'blog/index.html'
    queryset = Post.objects.all()

class PostDetail(generic.DetailView):
    model = Post

