# -*- coding: utf-8 -*-
from django.test import TestCase

from .model_instances import request


class TestRequest(TestCase):
    """
    A test case for a model `Request`
    """
    def setUp(self):
        self.request = request()

    def test_init(self):
        """
        Ensures that the instance of the `Request` model can be created
        """
        self.assertIsNotNone(self.request.pk, 'Should have an instance')

    def test_request_unicode(self):
        """
        Ensures that the method `__unicode__` of the `Request` model
        returns a valid string
        """
        self.request.url = u'/посилання/'
        self.request.save()
        self.assertEqual(self.request.__unicode__(),
                         u'%s %s /посилання/' % (
                             self.request.timestamp.isoformat(),
                             self.request.method
                         ),
                         'Method `__unicode__` of the `PersonInfo` model '
                         'should return a valid string')
