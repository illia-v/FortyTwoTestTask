from django.test import TestCase
from django.core.urlresolvers import resolve, reverse


class TestRequestsHistoryURLs(TestCase):
    def test_requests_history_view_url(self):
        """
        Ensures that a URL pattern name `requests_history` is valid and the
        pattern is resolved to `RequestsHistoryView`
        """
        requests_history = resolve('/requests_history/')

        self.assertEqual(reverse('requests_history'), '/requests_history/',
                         'A view name `requests_history` should be reversed '
                         'to the URL `/requests_history/`')
        self.assertEqual(requests_history.func.__name__, 'RequestsHistoryView',
                         'Should be resolved to `RequestsHistoryView`')

    def test_request_pulling_view_url(self):
        """
        Ensures that a URL pattern name `pull_new_requests` is valid
        and the pattern is resolved to `RequestsPullingView`
        """
        pulling = resolve('/pull_new_requests/')

        self.assertEqual(reverse('pull_new_requests'),
                         '/pull_new_requests/',
                         'A view name `pull_new_requests` should be '
                         'reversed to the URL `/pull_new_requests/`')
        self.assertEqual(pulling.func.__name__, 'RequestsPullingView',
                         'Should be resolved to `RequestsPullingView`')
