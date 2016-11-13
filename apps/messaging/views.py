import json

from django import http
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.formats import date_format
from django.views.generic import CreateView, FormView, TemplateView, View

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


class MessagingDetailView(MessagingViewWithInterlocutor, FormView):
    form_class = MessageForm
    template_name = 'messaging/detail.html'

    def get_messages(self):
        user = self.request.user
        interlocutor = self.get_interlocutor()

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
        context['interlocutor_username'] = self.get_interlocutor().username
        return context


def ajax_request(function):
    def wrapper(request, *args, **kwargs):
        if not request.is_ajax():
            return http.HttpResponseBadRequest()
        return function(request, *args, **kwargs)
    return wrapper


class MessagingCreateView(MessagingViewWithInterlocutor, CreateView):
    def get(self, request, *args, **kwargs):
        return http.HttpResponseNotAllowed(['POST'])

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            return http.HttpResponse(json.dumps(form.errors),
                                     content_type='application/json')

        try:
            conversation = Conversation.objects.filter(
                interlocutors__exact=request.user
            ).select_related('message_set').get(
                interlocutors__exact=self.get_interlocutor()
            )
        except ObjectDoesNotExist:
            raise http.Http404

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            body=self.get_message_body()
        )

        message_dict = {
            'id': message.id,
            'sender': message.sender.username,
            'body': message.body,
            'timestamp': date_format(message.timestamp, 'DATETIME_FORMAT')
        }

        return http.HttpResponse(json.dumps(message_dict),
                                 content_type='application/json')

    @method_decorator(ajax_request)
    def dispatch(self, *args, **kwargs):
        return super(MessagingCreateView, self).dispatch(*args, **kwargs)

    def get_form(self):
        return MessageForm({'message': self.get_message_body()})

    def get_message_body(self):
        try:
            return self.request.POST['message']
        except KeyError:
            return http.HttpResponseBadRequest()


class MessagingPullView(MessagingViewWithInterlocutor, View):
    def get(self, request, *args, **kwargs):
        interlocutor = self.get_interlocutor()

        try:
            messages = Conversation.objects.filter(
                interlocutors__exact=request.user
            ).select_related('message_set').get(
                interlocutors__exact=interlocutor
            ).message_set.all()
        except ObjectDoesNotExist:
            raise http.Http404

        last_message_id = self.get_last_message_id()
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

    @method_decorator(ajax_request)
    def dispatch(self, *args, **kwargs):
        return super(MessagingPullView, self).dispatch(*args, **kwargs)

    def get_last_message_id(self):
        try:
            return int(self.request.GET['last_message_id'])
        except (KeyError, ValueError):
            return http.HttpResponseBadRequest()


class MessagingUpdateUnreadCountView(View):
    def get(self, request, *args, **kwargs):
        return http.HttpResponse(
            self.get_interlocutors_with_unread_messages_count(),
            content_type='application/json'
        )

    @method_decorator(ajax_request)
    def dispatch(self, *args, **kwargs):
        return super(
            MessagingUpdateUnreadCountView, self
        ).dispatch(*args, **kwargs)

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
                {'interlocutor': interlocutor.username,
                 'unread_count': unread_count}
            )

        return json.dumps(interlocutors_with_unread_messages)
