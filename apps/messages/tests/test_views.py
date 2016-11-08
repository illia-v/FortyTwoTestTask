from django.test import RequestFactory, TestCase

from ..views import MessagesDetailView, MessagesIndexView
from hello.tests.model_instances import person_info


class TestMessagesIndexView(TestCase):
    """
    A test case for a view `MessagesIndexView`
    """
    def setUp(self):
        self.user = person_info()

    def test_messages_index_view_basic(self):
        """
        Ensures that `MessagesIndexView` uses an appropriate template and
        authenticated users can get its response
        """
        request = RequestFactory().get('/messages/')
        request.user = self.user
        response = MessagesIndexView.as_view()(request)

        self.assertTemplateUsed(response, 'messages/index.html',
                                'Should use an appropriate template')
        self.assertEqual(response.status_code, 200,
                         'Should be callable by a registered user')

    def test_anonymous(self):
        """
        Ensures that `MessagesIndexView` is not accessed when user is not
        authenticated
        """
        response_for_anonymous = self.client.get('/messages/')
        self.assertIn('login', response_for_anonymous.url,
                      'Should redirect to login')


class TestMessagesDetailView(TestCase):
    """
    A test case for a view `MessagesDetailView`
    """
    def setUp(self):
        self.user = person_info()
        self.interlocutor = person_info()

    def test_messages_detail_view_basic(self):
        """
        Ensures that `MessagesDetailView` uses an appropriate template and
        authenticated users can get its response
        """
        request = RequestFactory().get(
            '/messages/%s/' % self.interlocutor.username
        )
        request.user = self.user
        response = MessagesDetailView.as_view()(request)

        self.assertTemplateUsed(response, 'messages/detail.html',
                                'Should use an appropriate template')
        self.assertEqual(response.status_code, 200,
                         'Should be callable by a registered user')

    def test_anonymous(self):
        """
        Ensures that `MessagesDetailView` is not accessed when user is not
        authenticated
        """
        response_for_anonymous = self.client.get(
            '/messages/%s/' % self.interlocutor.username
        )
        self.assertIn('login', response_for_anonymous.url,
                      'Should redirect to login')
