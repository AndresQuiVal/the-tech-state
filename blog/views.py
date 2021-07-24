from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from .models import Post

class PostList(generic.ListView):
    template_name = 'blog/index.html'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['username'] = self.request.session.get('username', None)
        # add username context variable
        return context

class PostDetail(generic.DetailView):
    model = Post

# TODO: Change CRUD Post actions to Django REST

def delete_post(request, pk): 
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    # post deleted
    return redirect(reverse('blog:index-blog-view'))



