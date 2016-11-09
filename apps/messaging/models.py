from django.contrib.auth.models import User
from django.db import models


class Conversation(models.Model):
    interlocutors = models.ManyToManyField(User)

    def __unicode__(self):
        return '%s-%s' % (self.interlocutors.first().username,
                          self.interlocutors.last().username)


class Message(models.Model):
    conversation = models.ForeignKey(Conversation)
    sender = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.TextField(max_length=500)
    read = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s: %s' % (self.sender.username, self.body)
