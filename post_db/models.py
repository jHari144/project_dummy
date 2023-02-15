from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Posts(models.Model):
    post_title = models.CharField(max_length=100)
    post_text = models.CharField(max_length=800)
    pub_date = models.DateTimeField('date published')
    score = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    no_replies = models.IntegerField(default=0)
    def __str__(self): 
        return self.post_title

    def was_published_recently(self):
        return self.pub_date >= timezone.localtime(timezone.now()) - datetime.timedelta(days=1)

class Post_votes(models.Model):
    post_id = models.IntegerField(default = 0)
    user_id = models.IntegerField(default = 0)
    up_or_d = models.IntegerField(default = 0)

    def __str__(self): 
        return f"(Pid:{self.post_id}, Uid:{self.user_id})"

class Replies(models.Model):
    parent_id = models.IntegerField(default = 0)
    user_id = models.IntegerField(default = 0)
    score = models.IntegerField(default=0)
    reply_text = models.CharField(max_length=800)
    pub_date = models.DateTimeField('date published')

    def __str__(self): 
        return self.parent_id
