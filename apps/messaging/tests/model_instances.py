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


def message(conversation_for_message=None, sender=None):
    if not conversation_for_message:
        conversation_for_message = conversation()
    if not sender:
        sender = conversation_for_message.interlocutors.first()
    return models.Message.objects.create(
        conversation=conversation_for_message,
        sender=sender,
        body='Hello my friend!',
        read=False
    )
