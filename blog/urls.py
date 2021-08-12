from django.contrib import admin
from django.urls import path, include
from . import views

main_path = path('', views.PostList.as_view(), name = 'index-blog-view')

app_name = 'blog'
urlpatterns = [
    path('dashboard/', views.PostList.as_view(), name = 'index-blog-view'),
    path('posts/<int:pk>', views.PostDetail.as_view(), name = 'post-detail'),
    path('posts/<int:pk>/delete', views.delete_post, name = 'post-delete'),
    path('posts/<int:pk>/comment', views.comment_post, name = 'comment-post'),
    path('posts/<int:pk>/comment/<int:comment_pk>/upvote', views.upvote_comment, name = 'upvote-comment'),
    path('posts/<int:pk>/comment/<int:comment_pk>/downvote', views.downvote_comment, name = 'downvote-comment'),
    path('posts/<int:pk>/vote', views.vote_post, name = 'vote-post')
]
