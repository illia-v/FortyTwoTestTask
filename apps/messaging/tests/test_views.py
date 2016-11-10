from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase

from ..views import MessagingDetailView, MessagingIndexView


class TestMessagingIndexView(TestCase):
    """
    A test case for a view `MessagesIndexView`
    """
    def setUp(self):
        self.user = User.objects.create(username='test', password='testpswd')
        self.url = reverse('messaging:index')

    def test_messaging_index_view_basic(self):
        """
        Ensures that `MessagingIndexView` uses an appropriate template
        and authenticated users can get its response
        """
        request = RequestFactory().get(self.url)
        request.user = self.user
        response = MessagingIndexView.as_view()(request)

        self.assertTemplateUsed(response, 'messages/index.html',
                                'Should use an appropriate template')
        self.assertEqual(response.status_code, 200,
                         'Should be callable by a registered user')

    def test_anonymous(self):
        """
        Ensures that `MessagingIndexView` is not accessed when user is
        not authenticated
        """
        response_for_anonymous = self.client.get(self.url)
        self.assertIn('login', response_for_anonymous.url,
                      'Should redirect to login')


class TestMessagingDetailView(TestCase):
    """
    A test case for a view `MessagingDetailView`
    """
    def setUp(self):
        self.user = User.objects.create(username='test', password='testpswd')
        self.interlocutor = User.objects.create(username='test1',
                                                password='testpswd')
        self.url = reverse('messaging:detail',
                           args=[self.interlocutor.username])

    def test_messaging_detail_view_basic(self):
        """
        Ensures that `MessagingDetailView` uses an appropriate template and
        authenticated users can get its response
        """
        request = RequestFactory().get(self.url)
        request.user = self.user
        response = MessagingDetailView.as_view()(request)

        self.assertTemplateUsed(response, 'messaging/detail.html',
                                'Should use an appropriate template')
        self.assertEqual(response.status_code, 200,
                         'Should be callable by a registered user')

    def test_anonymous(self):
        """
        Ensures that `MessagesDetailView` is not accessed when user is not
        authenticated
        """
        response_for_anonymous = self.client.get(self.url)
        self.assertRedirects(
            response_for_anonymous,
            reverse('login') + '?next=%s' % self.url
        )
