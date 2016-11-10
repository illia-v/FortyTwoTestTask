import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet
from django.test import RequestFactory, TestCase

from .model_instances import message
from ..forms import MessageForm
from ..models import Conversation
from .. import views


class TestMessagingIndexView(TestCase):
    """
    A test case for a view `MessagesIndexView`
    """
    def setUp(self):
        self.user = User.objects.create(username='test', password='testpswd')
        request = RequestFactory().get('/messaging/')
        request.user = self.user
        self.response = views.MessagingIndexView.as_view()(request)

    def test_messaging_index_view_basic(self):
        """
        Ensures that `MessagingIndexView` uses an appropriate template
        and authenticated users can get its response
        """
        self.assertTemplateUsed(self.response, 'messages/index.html',
                                'Should use an appropriate template')
        self.assertEqual(self.response.status_code, 200,
                         'Should be callable by a registered user')

    def test_anonymous(self):
        """
        Ensures that `MessagingIndexView` is not accessed when user is
        not authenticated
        """
        response_for_anonymous = self.client.get('/messaging/')
        self.assertIn('login', response_for_anonymous.url,
                      'Should redirect to login')

    def test_messaging_index_view_returns_interlocutors(self):
        """
        Ensures that `MessagesIndexView` returns `QuerySet`
        `interlocutors_with_unread_messages_count` in context
        """
        interlocutors_with_unread_messages_count = self.response.context_data[
            'interlocutors_with_unread_messages_count'
        ]

        self.assertIs(type(interlocutors_with_unread_messages_count), list,
                      'Should return `list` '
                      '`interlocutors_with_unread_messages_count` in context')


class TestMessagingDetailView(TestCase):
    """
    A test case for a view `MessagingDetailView`
    """
    def setUp(self):
        self.interlocutor = User.objects.create(username='test1',
                                                password='testpswd')
        request = RequestFactory().get(
            '/messaging/%s/' % self.interlocutor.username
        )
        request.user = User.objects.create(username='test',
                                           password='testpswd')
        self.response = views.MessagingDetailView.as_view()(request)

    def test_messaging_detail_view_basic(self):
        """
        Ensures that `MessagingDetailView` uses an appropriate template and
        authenticated users can get its response
        """
        self.assertTemplateUsed(self.response, 'messaging/detail.html',
                                'Should use an appropriate template')
        self.assertEqual(self.response.status_code, 200,
                         'Should be callable by a registered user')

    def test_anonymous(self):
        """
        Ensures that `MessagesDetailView` is not accessed when user is not
        authenticated
        """
        response_for_anonymous = self.client.get(
            '/messaging/%s/' % self.interlocutor.username
        )
        self.assertIn('login', response_for_anonymous.url,
                      'Should redirect to login')

    def test_messaging_index_view_returns_messages(self):
        """
        Ensures that `MessagesIndexView` returns `QuerySet` `all_messages`
        in context
        """
        messages = self.response.context_data['all_messages']
        self.assertIs(type(messages), QuerySet,
                      'Should return `QuerySet` `all_messages` in context')

    def test_messaging_index_view_returns_message_form(self):
        """
        Ensures that `MessagesIndexView` returns a `MessageForm`
        instance in context
        """
        message_form = self.response.context_data['form']
        self.assertIs(type(message_form), MessageForm,
                      'Should return a `MessageForm` instance in context')

    def test_messaging_index_view_returns_interlocutor_username(self):
        """
        Ensures that `MessagesIndexView` returns `interlocutor_username`
        in context
        """
        self.assertIn('interlocutor_username', self.response.context_data,
                      'Should return `interlocutor_username` in context')


class TestMessagingCreateView(TestCase):
    """
    A test case for a view `MessagingCreateView`
    """
    def setUp(self):
        interlocutor = User.objects.create(username='test1',
                                           password='testpswd')
        self.user = User.objects.create(username='test', password='testpswd')

        self.conversation = Conversation.objects.create()
        self.conversation.interlocutors.add(self.user, interlocutor)
        self.conversation.save()

        self.url = reverse('messaging:create',
                           args=[interlocutor.username])

        request = RequestFactory().post(
            self.url,
            {'message_body': 'Hello world!'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        request.user = self.user
        self.response = views.MessagingCreateView.as_view()(request)

    def test_messaging_create_view_basic(self):
        """
        Ensures that authenticated users can get response of
        `MessagingCreateView`
        """
        self.assertEqual(self.response.status_code, 200,
                         'Should be callable by a registered user')

    def test_anonymous(self):
        """
        Ensures that `MessagingCreateView` is not accessed when user is
        not authenticated
        """
        response_for_anonymous = self.client.get(self.url)
        self.assertRedirects(
            response_for_anonymous,
            reverse('login') + '?next=%s' % self.url
        )

    def test_messaging_create_view_accepts_only_ajax_requests(self):
        """
        Ensures that `MessagingCreateView` raises HTTP error 400 if a
        request is not made via AJAX
        """
        request = RequestFactory().post(self.url,
                                        {'message_body': 'Hello world!'})
        request.user = self.user
        response = views.MessagingCreateView.as_view()(request)
        self.assertEqual(
            response.status_code, 400,
            'Should raise HTTP error 400 if a request is not made via AJAX'
        )

    def test_messaging_create_view_creates_message(self):
        """
        Ensures that `MessagingCreateView` creates a `Message` instance
        """
        message = self.conversation.message_set.first()
        self.assertIsNotNone(message, 'Should create a `Message` instance')
        self.assertEqual(message.body, 'Hello world!',
                         'Should create a message basing on request data')

    def test_messaging_create_view_returns_data_about_message(self):
        """
        Ensures that a JSON object returned by `MessagingCreateView`
        has all required data
        """
        message_data = json.loads(self.response.content)
        self.assertIsNotNone(message_data.get('id', None),
                             'Should contain `id` of a message')
        self.assertIsNotNone(message_data.get('body', None),
                             'Should contain `body` of a message')
        self.assertIsNotNone(message_data.get('sender', None),
                             'Should contain `sender` of a message')
        self.assertIsNotNone(message_data.get('timestamp', None),
                             'Should contain `timestamp` of a message')


class TestMessagingPullView(TestCase):
    def setUp(self):
        interlocutor = User.objects.create(username='test1',
                                           password='testpswd')
        self.user = User.objects.create(username='test', password='testpswd')

        conversation = Conversation.objects.create()
        conversation.interlocutors.add(self.user, interlocutor)
        conversation.save()

        for i in range(5):
            message(conversation)

        self.url = reverse('messaging:pull', args=[interlocutor.username])
        request = RequestFactory().get(
            self.url,
            {'last_message_id': 3},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        request.user = self.user
        self.response = views.MessagingPullView.as_view()(request)

        self.new_messages = json.loads(self.response.content)

    def test_messaging_pull_view_basic(self):
        """
        Ensures that authenticated users can get response of
        `MessagingPullView`
        """
        self.assertEqual(self.response.status_code, 200,
                         'Should be callable by a registered user')

    def test_anonymous(self):
        """
        Ensures that `MessagingPullView` is not accessed when user is
        not authenticated
        """
        response_for_anonymous = self.client.get(self.url)
        self.assertRedirects(
            response_for_anonymous,
            reverse('login') + '?next=%s' % self.url
        )

    def test_messaging_pull_view_accepts_only_ajax_requests(self):
        """
        Ensures that `MessagingPullView` raises HTTP error 400 if a
        request is not made via AJAX
        """
        request = RequestFactory().get(self.url, {'last_message_id': 3})
        request.user = self.user
        response = views.MessagingPullView.as_view()(request)
        self.assertEqual(
            response.status_code, 400,
            'Should raise HTTP error 400 if a request is not made via AJAX'
        )

    def test_messaging_pull_view_returns_all_new_messages(self):
        """
        Ensures that `MessagingPullView` returns all new messages
        and only them
        """
        self.assertEqual(len(self.new_messages), 2,
                         'Should return all new messages')
        for i in range(2):
            self.assertEqual(self.new_messages[i]['id'], i+4,
                             'Should return only new messages')

    def test_request_pull_view_returns_all_data(self):
        """
        Ensures that a JSON object returned by `MessagingPullView` has
        all required data
        """
        messages_data = self.new_messages[1]
        self.assertIsNotNone(messages_data.get('id', None),
                             'Should contain `id`s of a message')
        self.assertIsNotNone(messages_data.get('body', None),
                             'Should contain `body`s of messages')
        self.assertIsNotNone(messages_data.get('sender', None),
                             'Should contain `sender`s of messages')
        self.assertIsNotNone(messages_data.get('timestamp', None),
                             'Should contain `timestamp`s of messages')
