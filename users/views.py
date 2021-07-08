from django.db.models import query
from django.db.models.fields import files
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.views import generic
from django.http import Http404, HttpResponseBadRequest
from .services import DiscordService
from .helpers import UserHelper
from .models import UserDiscordModel, User
from django.urls import reverse
from .forms import CompleteNameForm, NewPostForm
from blog.models import File
from blog.models import Post


def validate_if_new_user(func): # decorator 

    def wrapper(*args, **kwargs):
        username = kwargs.get('username', None)
        if not username:
            return HttpResponseBadRequest("No username was provided")

        user_helper = UserHelper()
        not_new = user_helper.has_set_initial_user_info(username)
        if not_new == None: # user does not exist in database
            return Http404(f"User with {username} username does not exist")
        
        if not_new:
            return func(*args, **kwargs)
    
        return redirect(reverse('users:getting-started', args=(username,)))
    
    return wrapper


def login_view(request):
    """
    Returns the login view is user is not logged
    If a code param is given and its correct, it redirects to the user view
    If the user is logged in also redirects to the user view
    """

    user_helper = UserHelper()
    user_obj = user_helper.is_logged_in(request)
    user_discord_model = UserDiscordModel.create_user_discord_model(user_obj)
    
    if user_discord_model:
        return redirect(reverse('users:user-view', args=(user_discord_model.complete_username,)))

    code = request.GET.get('code', None)
    default_login_response = render(request, 'users/login.html', {})

    if not code:
        return default_login_response
   
    discord_service = DiscordService()
    response_token = discord_service.get_token_object(code)

    if not response_token:
        return default_login_response
    
    auth_code = response_token.get('access_token', None)
    user_obj = discord_service.get_current_user(auth_code)

    if not user_obj:
        return default_login_response
    
    user_discord_model = UserDiscordModel.create_user_discord_model(user_obj)
    
    # insert default data is user is not in db
    user_helper.insert_to_db_if_not_exists(user_discord_model)
    
    redirection = redirect(reverse('users:user-view', args=(user_discord_model.complete_username,)))
    redirection.set_cookie('access_token', auth_code)

    return redirection


@require_http_methods(['POST'])
def logout_view(request, username):
    """
    Logs out from the page
    """
    
    user_helper = UserHelper()
    user_obj = user_helper.is_logged_in_and_owner(request, username) # if they enter in url /logout they could possibly logout users
                                                                     # that's why is validated

    if not user_obj:
        raise HttpResponseBadRequest('You dont have access to log out this user!')
    
    response = redirect(reverse('users:login'))
    response.delete_cookie('access_token')

    # TODO: do more logout and session stuff...

    return response
    

@require_http_methods(["GET", "POST"])
@validate_if_new_user
def new_post(request, username):
    """
    Redirects to the new-post template
    """

    if not username:
        return HttpResponseBadRequest("Username is not provided")
    
    user_helper = UserHelper()
    if not user_helper.is_logged_in_and_owner(request, username):
        return redirect(reverse('blog:index-blog-view'))
    
    post_form = NewPostForm()

    if request.method == 'POST':
        post_form = NewPostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.populate_pending_data()

            # set user to post
            user = user_helper.exists_in_db(username)
            post.user = user
            post.save()

            # extract all files form the form
            files = request.FILES.getlist('post-files')

            if files:
                for file in files: # save file to file with the post related
                    file = File.objects.create(
                        post=post,
                        file=file
                    )
            
            return redirect(reverse('blog:index-blog-view'))

    context = {
        'post_form' : post_form
    }

    return render(request, 'users/new_post.html', context)


@validate_if_new_user
def user_view(request, username): # TODO: validate here the getting_started status of the user!!!
    """
    Redirects to the user view; if the user is the owner, enables edition permissions
    otherwise, enables view permissions (with restrictions)
    """

    if not username:
        raise HttpResponseBadRequest('The url given is not correct') # TODO: index of users view would be nice!

    user_helper = UserHelper()
    user_model = user_helper.exists_in_db(username)

    if not user_model:
        raise HttpResponseBadRequest('Bad request') # user should be in db

    context = {
        'user' : user_model
    }

    if not user_helper.is_logged_in_and_owner(request, username):
        return render(request, 'users/user.html', context)

    if not user_model.first_name and not user_model.last_name:
        return redirect(reverse('users:getting-started', args=(user_model.username,)))
    
    # enable edition permission
    context['is_owner'] = True
    return render(request, 'users/user.html', context)


class PostsIndex(generic.ListView):
    """
    Show the posts in index form
    """
    template_name = "users/post_list.html" # by default searches 'blog/post_list.html' beacuse Post model
                                           # is defined in such application
    def get_queryset(self):
        username = self.kwargs.get('username', None)
        queryset = []
        if not username:
            return queryset

        queryset = Post.objects.filter(user__username=username) 
        return queryset

def getting_started_view(request, username):
    """
    Redirects the template getting_started.html if its user's first time
    """

    user_helper = UserHelper()
    is_owner_and_logged_in = user_helper.is_logged_in_and_owner(request, username)

    if not is_owner_and_logged_in:
        return redirect(reverse('users:user-view', args=(username,)))

    user = User.objects.get(username=username)
    complete_name_form = CompleteNameForm()

    if request.method == 'POST': # form initial information
        complete_name_form = CompleteNameForm(request.POST)
        
        if complete_name_form.is_valid():
            user.first_name = complete_name_form.cleaned_data['first_name']
            user.last_name = complete_name_form.cleaned_data['last_name']
            user.save()

            return redirect(reverse('users:user-view', args=(username,)))


    context = {
        'user' : user,
        'complete_name_form' : complete_name_form
    }

    return render(request, 'users/getting_started.html', context)
    
