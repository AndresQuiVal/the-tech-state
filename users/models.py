from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    profile_img = models.CharField(max_length=150) # image will be the profile discord user image

    def get_full_name(self):
        return f'{str(self.first_name)} {str(self.last_name)}'

# external models 

class UserDiscordModel:

    def __init__(
        self, id, 
        username, discriminator, 
        avatar, email
    ):
        self.id = id
        self.username = username
        self.discriminator = discriminator

        if avatar is None: # no discord avatar available; select default profile image
            self._img_hash = 'media/default_profile_image.png'
            self.avatar_url = f'http://127.0.0.1:8000/{self._img_hash}'
        else:
            self._img_hash = avatar
            self.avatar_url = f'https://cdn.discordapp.com/avatars/{self.id}/{self._img_hash}'
        
        self.email = email
        self.complete_username = username + discriminator


    
    @classmethod
    def create_user_discord_model(cls, user_obj):
        """
        Creates a user discord model (UserDiscordModel) instance
        """
        if not user_obj:
            return None
        
        user_discord = UserDiscordModel(
            user_obj['id'], user_obj['username'],
            user_obj['discriminator'], user_obj['avatar'],
            user_obj['email']
        )

        return user_discord


class UserPostTemplate:

    def __init__(self, title, post_list):
        self.title = title
        self.post_list = post_list
    
    @classmethod
    def from_vote_model(cls, title, vote_queryset):
        """
        Create a UserPostTemplate model from a vote queryset
        """
        post_list = list(map(lambda e : e.post, vote_queryset))
        return UserPostTemplate(
            title=title,
            post_list=post_list
        )


class ResponseModel:
    """
    Model used for responses in services
    """

    def __init__(self, succeed, message, response_content):
        self.succeed =  succeed
        self.message = message
        self.response_content = response_content
    
    


