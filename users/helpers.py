"""
Defines a set of helpers for the app
"""

from .services import DiscordService
from .models import User, UserDiscordModel
import pdb

class UserHelper:

    def __init__(self):
        self.discord_service = DiscordService()

    def is_logged_in(self, request):
        """
        Verifies is the user is logged in by the request obj and the cookies

        Returns the complete user object dict if is logged in successfully
        """

        if not request:
            raise ValueError('No "request" was passed trough')
        
        if not request.session.has_key('access_token'):
            return False
        
        access_token = request.session['access_token'] 
        user_obj = self.discord_service.get_current_user(access_token) 

        if not user_obj: # TODO: refresh expired access tokens
            request.session.flush()
            return False
        
        if not 'id' in user_obj: # Does response dict returns another info if couldn't get the user correcty? for ensurance 
                                 # is created such validation
            return False
        
        return user_obj
    
    def is_logged_in_and_owner(self, request, username):
        """
        Validates if the user is logged in and the username matches with the logged-in user
        """
        user_obj = self.is_logged_in(request)
        if not user_obj:
            return False
        
        discord_model = UserDiscordModel.create_user_discord_model(user_obj)
        return discord_model.complete_username == username
    
    def insert_to_db_if_not_exists(self, discord_user : UserDiscordModel): # TODO: replace constants from first_name
                                                                   #       and last_name
        """
        Inserts a user into db if not presented
        Returns the User Model
        """
        try: 
            is_new = False
            user = User.objects.get(username=discord_user.complete_username)
        except User.DoesNotExist:
            user = User.objects.create(
                username=discord_user.complete_username,
                profile_img=discord_user.avatar_url,
                first_name='',
                last_name=''
            )
            is_new = True
        finally:
            return (is_new, user)
    
    def exists_in_db(self, username):
        """
        Verifies if the user exists in the db based on the username

        Returns the user if exists, else False
        """
        if not username:
            raise ValueError("Not 'username' parameter was provided")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return False
        else:
            return user
    
    def has_set_initial_user_info(self, username):
        """
        Verifies if the user has already set initial info. Initial info is (by now): First name, and Last name
        """
        if not username:
            raise ValueError("Not 'username' parameter was provided")
        
        user = self.exists_in_db(username)
        if not user:
            return None
        
        return user.first_name != '' and user.last_name != ''
    