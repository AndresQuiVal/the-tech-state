from django.contrib import admin
from django.urls import path, include
from .views import index_view 

main_path = path('', index_view, name = 'index-blog-view')

app_name = 'blog'
urlpatterns = [
    path('dashboard/', index_view, name = 'index-blog-view'),
]
