# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils.timezone import now

from ..models import ActionOnInstance


class TestActionOnInstance(TestCase):
    """
    A test case for a model `ActionOnInstance`
    """
    def setUp(self):
        self.action = ActionOnInstance.objects.create(
            model_name='Модель',
            app_name='застосунок',
            model_id=1,
            timestamp=now(),
            instance='{"field": "вміст"}',
            action=0
        )

    def test_init(self):
        """
        Ensures that the instance of the `ActionOnInstance` model can be
        created
        """
        self.assertIsNotNone(self.action.pk, 'Should have an instance')

    def test_instance_action_unicode(self):
        """
        Ensures that the method `__unicode__` of the `ActionOnInstance`
        model returns a valid string
        """
        str_representation = '%s %s `%s.%s.%d`' % (
            self.action.timestamp.isoformat(),
            self.action.get_action_display(),
            self.action.app_name,
            self.action.model_name,
            self.action.model_id
        )
        self.assertEqual(self.action.__unicode__(), str_representation,
                         'Method `__unicode__` of the `ActionOnInstance` '
                         'model should return a valid string')
