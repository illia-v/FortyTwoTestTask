import json

from django import http
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.utils.formats import date_format
from django.views.generic import FormView, TemplateView, View

from .forms import MessageForm
from .models import Conversation, Message


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
                ).message_set.filter(read=False, sender=interlocutor).count()
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


class MessagingViewWithInterlocutor(object):
    def get_interlocutor(self):
        """Gets a `User` instance interlocutor from a path of a request"""
        interlocutors_username = self.request.path.split('/')[2]
        return get_object_or_404(User, username=interlocutors_username)


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
        context['all_messages'] = self.get_messages()
        context['interlocutor_username'] = self.get_interlocutor_username()
        return context


class MessagingCreateView(View):
    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return http.HttpResponseBadRequest()

        try:
            message_body = request.POST['message']
        except KeyError:
            return http.HttpResponseBadRequest()

        form = MessageForm({'message': message_body})
        if not form.is_valid():
            return http.HttpResponse(json.dumps(form.errors),
                                     content_type='application/json')

        # interlocutor's username from a path of a request
        interlocutors_username = request.path.split('/')[2]
        interlocutor = get_object_or_404(User, username=interlocutors_username)

        try:
            conversation = Conversation.objects.filter(
                interlocutors__exact=request.user
            ).select_related('message_set').get(
                interlocutors__exact=interlocutor
            )
        except ObjectDoesNotExist:
            raise http.Http404

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            body=message_body
        )

        message_dict = {
            'id': message.id,
            'sender': message.sender.username,
            'body': message.body,
            'timestamp': date_format(message.timestamp, 'DATETIME_FORMAT')
        }

        return http.HttpResponse(json.dumps(message_dict),
                                 content_type='application/json')


class MessagingPullView(View):
    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            return http.HttpResponseBadRequest()

        try:
            last_message_id = int(request.GET['last_message_id'])
        except (KeyError, ValueError):
            return http.HttpResponseBadRequest()

        # interlocutor's username from a path of a request
        interlocutors_username = request.path.split('/')[2]
        interlocutor = get_object_or_404(User, username=interlocutors_username)

        try:
            messages = Conversation.objects.filter(
                interlocutors__exact=request.user
            ).select_related('message_set').get(
                interlocutors__exact=interlocutor
            ).message_set.all()
        except ObjectDoesNotExist:
            raise http.Http404

        # If a clients page is up to date
        if messages.last() is None or messages.last().id == last_message_id:
            return http.HttpResponse('[]', content_type='application/json')

        new_messages = []

        for new_message in messages.filter(id__gt=last_message_id).\
                order_by('id'):
            sender = (new_message.sender.username
                      if new_message.sender != request.user else 'You')
            new_messages.append({
                'id': new_message.id,
                'sender': sender,
                'body': new_message.body,
                'timestamp': date_format(new_message.timestamp,
                                         'DATETIME_FORMAT')
            })

        return http.HttpResponse(json.dumps(new_messages),
                                 content_type='application/json')
