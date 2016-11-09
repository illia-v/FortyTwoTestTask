from django.test import TestCase
from django.core.urlresolvers import resolve, reverse


class TestMessagingURLs(TestCase):
    def test_messages_index_view_url(self):
        """
        Ensures that a URL pattern name `messaging` is valid and the
        pattern is resolved to `MessagingIndexView`
        """
        messages = resolve('/messaging/')

        self.assertEqual(reverse('messaging:index'), '/messaging/',
                         'A view name `messaging:index` should be reversed to '
                         'the URL `/messaging/`')
        self.assertEqual(messages.func.__name__, 'MessagingIndexView',
                         'Should be resolved to `MessagingIndexView`')

    def test_messages_detail_view_url(self):
        """
        Ensures that a URL pattern name `messages_detail` is valid and
        the pattern is resolved to `MessagingDetailView`
        """
        messages_detail = resolve('/messaging/somebody/')

        self.assertEqual(reverse('messaging:detail', args=['somebody']),
                         '/messaging/somebody/',
                         'A view name `messaging:detail` should be reversed '
                         'to the URL `/messaging/{username}/`')
        self.assertEqual(messages_detail.func.__name__, 'MessagingDetailView',
                         'Should be resolved to `MessagingDetailView`')
