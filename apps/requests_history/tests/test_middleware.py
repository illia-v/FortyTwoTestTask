from django.test import RequestFactory, TestCase

from ..middleware import RequestSavingMiddleware
from ..models import Request


class TestRequestSavingMiddleware(TestCase):
    """
    A test case for a middleware class `RequestSavingMiddleware`
    """
    def test_request_saving_middleware_creates_request_instance(self):
        """
        Ensures that `RequestSavingMiddleware` creates a `Request`
        instance basing on a request
        """
        RequestSavingMiddleware().process_request(RequestFactory().get('/'))
        self.assertEqual(Request.objects.all().count(), 1,
                         'Should create a `Request` instance')
        self.assertEqual(Request.objects.get(pk=1).url, '/', 'Should create '
                         'a `Request` instance basing on a request')

    def test_this_middleware_not_saves_requests_via_ajax(self):
        """
        Ensures that `RequestSavingMiddleware` does not save requests
        made using AJAX
        """
        RequestSavingMiddleware().process_request(
            RequestFactory().get('/pull_with_new_requests/',
                                 HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        )
        self.assertEqual(Request.objects.all().count(), 0,
                         'Should not save requests made using AJAX')
