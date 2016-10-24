import json

from django.db.models.query import QuerySet
from django.test import RequestFactory, TestCase

from .model_instances import request
from .. import views
from ..models import Request


class TestRequestsHistoryView(TestCase):
    """
    A test case for a view `RequestsHistoryView`
    """
    def setUp(self):
        for i in range(11):
            request()
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

    def test_requests_history_view_returns_requests(self):
        """
        Ensures that `RequestsHistoryView` returns 10 `Request`
        instances in context
        """
        requests = self.response.context_data['requests']
        self.assertIs(type(requests), QuerySet, 'Should return `QuerySet` '
                      '`requests` in context')
        self.assertEqual(len(requests), 10, 'Should return only 10 '
                         '`PersonInfo` instances `requests` in `QuerySet`')

    def test_requests_history_view_returns_only_10_last_requests(self):
        """
        Ensures that `RequestsHistoryView` returns only last 10
        `Request` instances in context
        """
        requests = self.response.context_data['requests']
        self.assertEqual(list(requests),
                         list(Request.objects.all().order_by('-id')[:10]),
                         'Should return only last 10 `Request` instances in '
                         'context')


class TestRequestsPullingView(TestCase):
    def setUp(self):
        for i in range(12):
            request()
        response = views.RequestsPullingView.as_view()(
            RequestFactory().get('/', {'last_request_id': 10})
        )
        self.new_requests = json.loads(response.content)

    def test_request_pulling_view_returns_all_new_requests(self):
        """
        Ensures that `RequestsHistoryView` returns all new requests and
        only them
        """
        self.assertEqual(len(self.new_requests), 2,
                         'Should return all new requests')
        for i in range(2):
            self.assertEqual(self.new_requests[i]['id'], i+11,
                             'Should return only new requests')

    def test_request_pulling_view_returns_all_data(self):
        """
        Ensures that a JSON object returned by `RequestsHistoryView` has
        all required data
        """
        request = self.new_requests[1]
        self.assertIsNotNone(request.get('id', None),
                             'Should contain requests `id`s')
        self.assertIsNotNone(request.get('url', None),
                             'Should contain requests `url`s')
        self.assertIsNotNone(request.get('method', None),
                             'Should contain requests `method`s')
        self.assertIsNotNone(request.get('timestamp', None),
                             'Should contain requests `timestamps`s')
        self.assertIsNotNone(request.get('priority', None),
                             'Should contain requests `priority`')
