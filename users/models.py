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
        self._img_hash = avatar
        self.email = email

        self.complete_username = username + discriminator
        self.avatar_url = f'https://cdn.discordapp.com/avatars/{self.id}/{self._img_hash}'

    
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


class ResponseModel:
    """
    Model used for responses in services
    """

    def __init__(self, succeed, message, response_content):
        self.succeed, self.message, self.response_content = succeed, message, response_content
    
    


