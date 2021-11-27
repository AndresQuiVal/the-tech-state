from django.shortcuts import get_object_or_404, get_list_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.http.response import Http404, HttpResponseBadRequest
from django.views import generic
from django.urls import reverse
from users.helpers import UserHelper
from users.models import User
from .models import Comment, Post

class PostList(generic.ListView):
    template_name = 'blog/index.html'
    section = "Feed"

    def get_context_data(self, **kwargs):
        global section
        context = super(PostList, self).get_context_data(**kwargs)
        context['username'] = self.request.session.get('username', None)
        context['section'] = section
        # add username context variable
        return context
    
    def get_queryset(self):
        global section
        section = self.request.GET.get('section', '')
        search = self.request.GET.get('searchTerm', '')

        if section:
            section = section.lower()
            queryset = Post.objects.filter(section=section)
        else:
            section = "Feed"
            queryset = Post.objects.all()

        # apply search term

        return queryset.filter(title__icontains=search) | queryset.filter(user__username__icontains=search)
        
class PostDetail(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['max_attachments'] = 3
        # add username context variable
        return context

# TODO: Change CRUD Post actions to Django REST

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user_logged_in = UserHelper().get_user_logged_in(request)

    if user_logged_in.complete_username != post.user.username:
        return HttpResponseBadRequest("Cannot delete other's posts")
        
    post.delete()
    # post deleted
    return redirect(reverse('blog:index-blog-view'))

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user_logged_in = UserHelper().get_user_logged_in(request)

    if user_logged_in.complete_username != post.user.username:
        return HttpResponseBadRequest("Cannot edit other's posts")
    
    # post deleted
    return redirect(reverse('blog:index-blog-view'))

@require_http_methods(['POST'])
def comment(request, pk, comment_pk = -1):
    """
    Comments either a post or a comment
    NOTE: only admits commenting a single comment
    """
    username = request.session.get("username", None)
    if not username:
        return redirect(reverse("users:login"))
    
    user = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=pk)
    content = request.POST.get('content', None)

    if not content:
        return HttpResponseBadRequest("The content cannot be null!")
    
    comment = Comment()
    comment.populate_pending_data()
    comment.post = post
    comment.user = user
    comment.content = content
    
    if comment_pk != -1:
        comment_replied = get_object_or_404(Comment, pk=comment_pk)
        if comment_replied.is_reply():
            # users shouldn't reply a comment
            return HttpResponseBadRequest("Reply comment cannot be replied again. ")

        comment.comment_replied = comment_replied

    comment.save()

    return redirect(reverse("blog:post-detail", args=(pk,)))


@require_http_methods(['POST'])
def upvote_comment(request, pk, comment_pk): # TODO: validate likes by user
                                             # such that when liked a comment, automatically
                                             # remove dislike, and viceversa
    post = get_object_or_404(Post, pk=pk)
    comment = post.comment_set.get(pk=comment_pk)
    comment.upvotes += 1
    comment.save()

    return redirect(reverse("blog:post-detail", args=(pk,)))


@require_http_methods(['POST'])
def downvote_comment(request, pk, comment_pk):
    post = get_object_or_404(Post, pk=pk)
    comment = post.comment_set.get(pk=comment_pk)
    comment.downvotes += 1
    comment.save()

    return redirect(reverse("blog:post-detail", args=(pk,)))


@require_http_methods(['POST'])
def vote_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not 'username' in request.session:
        return redirect(reverse("users:login"))
    
    username = request.session['username']
    is_upvoted = request.GET.get('upvote', True)
    if is_upvoted == 'True':
        post.get_votes().upvote(username)
    else:
        post.get_votes().downvote(username)

    return redirect(reverse('blog:post-detail', args=(pk,)))


