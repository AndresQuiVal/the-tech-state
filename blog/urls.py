from django.contrib import admin
from django.urls import path, include
from . import views

main_path = path('', views.PostList.as_view(), name = 'index-blog-view')

app_name = 'blog'
urlpatterns = [
    path('dashboard/', views.PostList.as_view(), name = 'index-blog-view'),
    path('posts/<int:pk>', views.PostDetail.as_view(), name = 'post-detail'),
    path('posts/<int:pk>/delete', views.delete_post, name = 'post-delete')
]
