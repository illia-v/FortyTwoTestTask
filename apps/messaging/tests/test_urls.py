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

    def test_messaging_create_view_url(self):
        """
        Ensures that a URL pattern name `messaging:create` is valid and
        the pattern is resolved to `MessagingCreateView`
        """
        messaging_create = resolve('/messaging/somebody/new/')

        self.assertEqual(reverse('messaging:create', args=['somebody']),
                         '/messaging/somebody/new/',
                         'A view name `messaging:create` should be reversed '
                         'to the URL `/messaging/{username}/new/`')
        self.assertEqual(messaging_create.func.__name__, 'MessagingCreateView',
                         'Should be resolved to `MessagingCreateView`')

    def test_messaging_pull_view_url(self):
        """
        Ensures that a URL pattern name `messaging:pull` is valid and
        the pattern is resolved to `MessagingPullView`
        """
        messaging_pull = resolve('/messaging/somebody/pull/')

        self.assertEqual(reverse('messaging:pull', args=['somebody']),
                         '/messaging/somebody/pull/',
                         'A view name `messaging:pull` should be reversed '
                         'to the URL `/messaging/{username}/pull/`')
        self.assertEqual(messaging_pull.func.__name__, 'MessagingPullView',
                         'Should be resolved to `MessagingPullView`')

    def test_messaging_update_unread_count_view_url(self):
        """
        Ensures that a URL pattern name `messaging:update_unread_count`
        is valid and the pattern is resolved to
        `MessagingUpdateUnreadCountView`
        """
        update_unread_count = resolve(
            '/messaging/update_unread_count/'
        )

        self.assertEqual(
            reverse('messaging:update_unread_count'),
            '/messaging/update_unread_count/',
            'A view name `messaging:update_unread_count` should be reversed '
            'to the URL `/messaging/update_unread_count/`'
        )
        self.assertEqual(
            update_unread_count.func.__name__,
            'MessagingUpdateUnreadCountView',
            'Should be resolved to `MessagingUpdateUnreadCountView`'
        )

    def test_messaging_reset_unread_count_view_url(self):
        """
        Ensures that a URL pattern name `messaging:reset_unread_count`
        is valid and the pattern is resolved to
        `MessagingResetUnreadCountView`
        """
        reset_unread_count = resolve(
            '/messaging/somebody/reset_unread_count/'
        )

        self.assertEqual(
            reverse('messaging:reset_unread_count', args=['somebody']),
            '/messaging/somebody/reset_unread_count/',
            'A view name `messaging:update_unread_count` should be reversed '
            'to the URL `/messaging/{username}/reset_unread_count/`'
        )
        self.assertEqual(
            reset_unread_count.func.__name__,
            'MessagingResetUnreadCountView',
            'Should be resolved to `MessagingResetUnreadCountView`'
        )
