from django.contrib.auth.models import User

from .. import models


def conversation():
    user1 = User.objects.create(username='test', password='testpswd')
    user2 = User.objects.create(username='test1', password='testpswd')
    return models.Conversation.objects.create(interlocutors=[user1, user2])


def message():
    return models.Message.objects.create(
        conversation=conversation(),
        sender=conversation().interlocutors.first(),
        body='Hello my friend!',
        read=False
    )
