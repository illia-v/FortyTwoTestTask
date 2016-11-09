from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.test import RequestFactory, TestCase

from ..forms import MessageForm
from ..views import MessagingDetailView, MessagingIndexView


class TestMessagingIndexView(TestCase):
    """
    A test case for a view `MessagesIndexView`
    """
    def setUp(self):
        self.user = User.objects.create(username='test', password='testpswd')
        request = RequestFactory().get('/messaging/')
        request.user = self.user
        self.response = MessagingIndexView.as_view()(request)

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
        self.response = MessagingDetailView.as_view()(request)

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
        Ensures that `MessagesIndexView` returns `QuerySet` `messages`
        in context
        """
        messages = self.response.context_data['messages']
        self.assertIs(type(messages), QuerySet,
                      'Should return `QuerySet` `messages` in context')

    def test_messaging_index_view_returns_message_form(self):
        """
        Ensures that `MessagesIndexView` returns a `MessageForm`
        instance in context
        """
        message_form = self.response.context_data['form']
        self.assertIs(type(message_form), MessageForm,
                      'Should return a `MessageForm` instance in context')
