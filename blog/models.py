from datetime import datetime
from users.models import User
from django.db import models
import uuid


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
    upvotes = models.IntegerField(default=0, blank=True)
    downvotes = models.IntegerField(default=0, blank=True)


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


class Comment(models.Model):

    class Meta:
        unique_together = (('comment_id', 'post', 'user'),)

    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()
    datetime = models.DateTimeField()
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()



class File(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        blank=True, null=True)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE,
        blank=True, null=True)
    file = models.FileField(upload_to=upload_to)