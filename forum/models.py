from django.db import models
from django.contrib.auth.models import  AbstractUser, User
import datetime


class Tags(models.Model):
   tag = models.CharField(max_length=50)

   def __str__(self):
        return self.tag

class ForumPost(models.Model):
    sno = models.AutoField(primary_key=True)
    # title = models.CharField(max_length = 255)
    # brief_description = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete =models.CASCADE)
    # slug = models.CharField(max_length=130)
    timestamp = models.DateTimeField(blank=False, default=datetime.datetime.now())
    thumbnail = models.ImageField('thumbnails')
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return str(self.timestamp) +' '+ 'by' + '   @'+self.author.username



class ForumComment(models.Model):
    sno = models.AutoField(primary_key=True)
    # name = models.CharField(max_length=39)
    # email = models.EmailField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=69, null=True)
    message = models.TextField()
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True) # subcomments
    timestamp = models.DateTimeField(default=datetime.datetime.now())
    # comment = models.TextField()
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)# subcomment