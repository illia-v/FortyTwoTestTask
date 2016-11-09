from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, TemplateView

from .forms import MessageForm
from .models import Conversation


class MessagingIndexView(TemplateView):
    template_name = 'messaging/index.html'

    def get_interlocutors_with_unread_messages_count(self):
        user = self.request.user
        interlocutors_with_unread_messages = []

        for interlocutor in User.objects.exclude(pk=user.pk).iterator():
            try:
                unread_count = Conversation.objects.filter(
                    interlocutors__exact=user
                ).select_related('message_set').get(
                    interlocutors__exact=interlocutor
                ).message_set.filter(read=False).count()
            except ObjectDoesNotExist:
                unread_count = 0

            interlocutors_with_unread_messages.append(
                (interlocutor, unread_count)
            )

        return interlocutors_with_unread_messages

    def get_context_data(self, **kwargs):
        context = super(MessagingIndexView, self).get_context_data(**kwargs)
        context['interlocutors_with_unread_messages_count'] = (
            self.get_interlocutors_with_unread_messages_count()
        )
        return context


class MessagingDetailView(FormView):
    form_class = MessageForm
    template_name = 'messaging/detail.html'

    def get_interlocutor_username(self):
        """Gets interlocutor's username from a path of a request"""
        return self.request.path.split('/')[2]

    def get_messages(self):
        user = self.request.user
        interlocutor = get_object_or_404(
            User, username=self.get_interlocutor_username()
        )

        try:
            conversation = Conversation.objects.filter(
                interlocutors__exact=user
            ).select_related('message_set').get(
                interlocutors__exact=interlocutor
            )
        except ObjectDoesNotExist:
            conversation = Conversation.objects.create()
            conversation.interlocutors.add(user, interlocutor)
            conversation.save()

        return conversation.message_set.all().order_by('timestamp')

    def get_context_data(self, **kwargs):
        context = super(MessagingDetailView, self).get_context_data(**kwargs)
        context['messages'] = self.get_messages()
        context['interlocutor_username'] = self.get_interlocutor_username()
        return context
