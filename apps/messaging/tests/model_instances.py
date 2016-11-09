import random
import string

from django.contrib.auth.models import User

from .. import models


def conversation():
    def random_username():
        return ''.join(
            (random.choice(string.ascii_lowercase) for i in range(10))
        )

    conversation = models.Conversation.objects.create()
    conversation.interlocutors.add(
        User.objects.create(username=random_username()),
        User.objects.create(username=random_username())
    )
    return conversation


def message():
    return models.Message.objects.create(
        conversation=conversation(),
        sender=conversation().interlocutors.first(),
        body='Hello my friend!',
        read=False
    )
