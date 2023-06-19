from typing import Text
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Contact(models.Model): #author
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    friend = models.ManyToManyField('self', blank=True, default=None)
    image = models.ImageField(upload_to='user_images', null=True, default='/triangle.jpg')
    def __str__(self):
        return self.user.username
        
class Message(models.Model):
    contact = models.ForeignKey(Contact, related_name='author', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.username


class Chat(models.Model): #curretly you're chating with
    participants = models.ManyToManyField(Contact)
    messages = models.ManyToManyField(Message, blank = True)
    
    def last_30_messages(self):
        return self.messages.all()
        # return "boo"
        # return self.messages.objects.order_by('timestamp').all()[:30]

            
    def __str__(self):
        # return "{}".format(self.pk) 
        return str(self.participants.all())

