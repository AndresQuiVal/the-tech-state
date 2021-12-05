"""
Defines all the third party services
"""
import requests
import pdb

class DiscordService:
    """
    Define all helpers that handle discord service 
    """
    API_ENDPOINT = 'https://discord.com/api/v8'
    CLIENT_ID = '833554127652519957'
    CLIENT_SECRET = 'BCL-y0K563MiTX_FRqeHhgXgYiurqoeI'
    REDIRECT_URI = 'https://thetechstate.herokuapp.com/users/login'

    def get_token_object(self, code):
        """
        Returns the token object, with access token, etc
        """
        data = {
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.REDIRECT_URI
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            response = requests.post(f'{self.API_ENDPOINT}/oauth2/token', data=data, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            return False
        else:
            return response.json()
    

    def refresh_token_object(self, refresh_token):
        """
        Returns a token object when the previous access token expired
        """
        data = {
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            response = requests.post(f'{self.API_ENDPOINT}/oauth2/token', data=data, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError:           
            return False
        else:
            return response.json()
    

    def get_current_user(self, auth_code):
        """
        Returns the current user information
        """
        if not auth_code:
            return False
            
        headers = {
            'Authorization' : f'Bearer {auth_code}'
        }

        try:
            response = requests.get('http://discordapp.com/api/users/@me', headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            return False
        except Exception as ex:
            pass
        else:
            return response.json()