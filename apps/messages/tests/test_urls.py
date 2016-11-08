from django.test import TestCase
from django.core.urlresolvers import resolve, reverse


class TestMessagesURLs(TestCase):
    def test_messages_index_view_url(self):
        """
        Ensures that a URL pattern name `messages` is valid and the
        pattern is resolved to `MessagesIndexView`
        """
        messages = resolve('/messages/')

        self.assertEqual(reverse('messages'), '/messages/',
                         'A view name `messages` should be reversed to the '
                         'URL `/messages/`')
        self.assertEqual(messages.func.__name__, 'MessagesIndexView',
                         'Should be resolved to `MessagesIndexView`')

    def test_messages_detail_view_url(self):
        """
        Ensures that a URL pattern name `messages_detail` is valid and
        the pattern is resolved to `MessagesDetailView`
        """
        messages_detail = resolve('/messages/somebody/')

        self.assertEqual(reverse('messages_detail', args=('somebody')),
                         '/messages/somebody/',
                         'A view name `messages_detail` should be reversed to '
                         'the URL `/messages/{username}/`')
        self.assertEqual(messages_detail.func.__name__, 'MessagesDetailView',
                         'Should be resolved to `MessagesDetailView`')
