from datetime import datetime

from django.db.models.fields import related
from django.utils import tree
from users.models import User
from django.db import models
import uuid

# managers

class VoteManager(models.Manager):

    def _get_votes_by_upvoted(self, is_upvoted):
        return super().get_queryset().filter(is_upvoted=is_upvoted)
    
    @property
    def number_upvotes(self):
        return len(self.upvoted_posts)
    
    @property
    def number_downvotes(self):
        return len(self.downvoted_posts)
    
    @property
    def upvoted_posts(self):
        return self._get_votes_by_upvoted(True)
    
    @property 
    def downvoted_posts(self):
        return self._get_votes_by_upvoted(False)





def upload_to(instance, filename):
    filename = str(uuid.uuid4())
    return '%s/%s' %(instance.post.user.username, filename)

class Post(models.Model):

    class Meta:
        unique_together = (('post_id', 'user'),)
    
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    section = models.PositiveIntegerField(
        choices=(
            (1, "Codigo"),
            (2, "Diseño"),
            (3, "Blockchain"),
            (4, "Emprendimiento")
        ))
        
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    summary = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    votes = models.ManyToManyField(User, related_name="voted_posts",
                                         through='Vote')

    votes_ins = None

    class Votes:
        """
        Refers to the Votes related to the post
        """

        def __init__(self, post):
            self.post = post
            self.votes = Vote.objects.filter(post__pk=post.post_id)
            self.__set_upvotes_and_downvotes()

        def __set_upvotes_and_downvotes(self):
            self.upvotes, self.downvotes = 0, 0
            for vote in self.votes:
                if vote.is_upvoted:
                    self.upvotes += 1
                else:
                    self.downvotes += 1

        def __vote(self, username, is_upvoted):
            try: 
                user_vote = Vote.objects.get(
                    post__pk=self.post.post_id, user__username=username)
            except Vote.DoesNotExist:
                user_vote = Vote.objects.create(
                    post = self.post, user = User.objects.get(username=username)
                )
            finally:
                user_vote.is_upvoted = is_upvoted
                user_vote.save()
                self.__set_upvotes_and_downvotes()

        def upvote(self, username):
            self.__vote(username, True)
            
        def downvote(self, username):
            self.__vote(username, False)
        

    def populate_pending_data(self):
        """
        Deletes code repetition by setting basic data automatically
        """
        self.datetime = datetime.now()
        self.summary = str(self.content)[:50]


    def save(self, *args, **kwargs):
        """
        Saves the instance to db, but performs extra validation
        """
        content_str = str(self.content)
        if len(content_str) < 50:
            raise ValueError("Content cannot be of 50 characters")

        super(Post, self).save(*args, **kwargs)

    def get_votes(self):
        if not self.votes_ins:
            self.votes_ins = self.Votes(self)
        
        return self.votes_ins


class Vote(models.Model):

    objects = VoteManager()

    # compound key
    post = models.ForeignKey(Post, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # related fields
    is_upvoted = models.BooleanField(default=True)



class Comment(models.Model):

    class Meta:
        unique_together = (('comment_id', 'post', 'user'),)

    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    content = models.TextField()
    datetime = models.DateTimeField()
    upvotes = models.IntegerField(default=0, blank=True)
    downvotes = models.IntegerField(default=0, blank=True)
    comment_replied = models.ForeignKey("self", on_delete=models.CASCADE, 
                                        blank=True, null=True, related_name="replies")

    def populate_pending_data(self):
        """
        Deletes code repetition by setting basic data automatically
        """
        self.datetime = datetime.now()
    
    
    def is_reply(self):
        """
        Validates if the current comment is a reply based on the 
        comment_replied field value
        """
        return bool(self.comment_replied)


class File(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="attachments",
        blank=True, null=True)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="attachments",
        blank=True, null=True)
    file = models.FileField(upload_to=upload_to)


