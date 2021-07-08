from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name = 'login'),
    path('<username>/', views.user_view, name = 'user-view'),
    path('<username>/logout/', views.logout_view, name = 'logout'),
    path('<username>/getting-started/', views.getting_started_view, name = 'getting-started'),
    path('<username>/new-post/', views.new_post, name = 'new-post'),
    path('<username>/posts/', views.PostsIndex.as_view(), name = 'posts')
]