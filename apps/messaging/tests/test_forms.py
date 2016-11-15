import random
import string

from django.test import TestCase

from ..forms import MessageForm


class TestMessageForm(TestCase):
    def setUp(self):
        self.form = MessageForm

    def test_message_form_with_no_data(self):
        """
        Ensures that `MessageForm` is invalid if no data is given
        """
        self.assertFalse(self.form(data={}).is_valid(),
                         'Should be invalid if no data is given')

    def test_message_form_with_sufficient_data(self):
        """
        Ensures that `MessageForm` is valid if sufficient data is given
        """
        self.assertTrue(self.form(data={'body': 'Hello world!'}),
                        'Should be valid if sufficient data is given')

    def test_message_form_with_too_long_message(self):
        """
        Ensures that `MessageForm` is invalid if a message is too long
        """
        self.assertFalse(self.form(
            data={'body': '    '.join(
                (random.choice(string.ascii_lowercase) for i in range(127)))
            }).is_valid(),
            'Should be invalid if a message is too long'
        )
