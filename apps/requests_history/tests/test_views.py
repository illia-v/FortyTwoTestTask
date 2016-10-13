from django.test import RequestFactory, TestCase

from .. import views


class TestRequestsHistoryView(TestCase):
    """
    A test case for a view `RequestsHistoryView`
    """
    def setUp(self):
        self.response = views.RequestsHistoryView.as_view()(
            RequestFactory().get('/requests_history/')
        )

    def test_requests_history_view_basic(self):
        """
        Ensures that `RequestsHistoryView` uses an appropriate template
        and everyone could get its response
        """
        self.assertTemplateUsed(self.response,
                                'requests_history/index.html',
                                'Should use an appropriate template')
        self.assertEqual(self.response.status_code, 200,
                         'Should be callable by anyone')
