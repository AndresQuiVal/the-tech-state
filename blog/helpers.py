"""
Defines helpers for the blog app (or external apps as 'users')
"""

from models import Post

class PostRequest:
    """
    Superset model of Post
    """

    def get_all_by_filtered_owner(self, request):
        posts = super().objects.all()
        for i in range  # TODO: finish filtering by owner all posts such to avouid issue #11
            pass

        
