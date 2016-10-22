from datetime import date
from StringIO import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase

from ..forms import HelloEditForm
from .image import TEST_IMAGE


class TestHelloEditForm(TestCase):
    def setUp(self):
        self.form = HelloEditForm

    def test_hello_edit_form_with_no_data(self):
        """
        Ensures that `HelloEditForm` is invalid if no data is given
        """
        self.assertFalse(self.form(data={}).is_valid(),
                         'Should be invalid if no data is given')

    def test_hello_edit_form_with_insufficient_data(self):
        """
        Ensures that `HelloEditForm` is invalid if insufficient data is
        given
        """
        form_data = {'first_name': 'John', 'second_name': 'Fake'}
        self.assertFalse(self.form(data=form_data).is_valid(),
                         'Should be invalid if insufficient data is given')

    def test_hello_edit_form_with_sufficient_data(self):
        """
        Ensures that `HelloEditForm` is valid if sufficient data is
        given
        """
        form_data = {
            'first_name': 'John', 'second_name': 'Fake',
            'birth_date': date(year=1900, month=1, day=1), 'bio': 'my bio',
            'email': 'john@fake.com', 'jabber': 'john@fake.com',
            'skype': 'john_fake', 'other_contacts': 'nothing',
        }
        form_files = {
            'photo':  InMemoryUploadedFile(
                          StringIO(TEST_IMAGE),
                          field_name='photo',
                          name='my_photo.jpg',
                          content_type='image/jpg',
                          size=len(TEST_IMAGE),
                          charset='utf-8',
                      )
        }
        self.assertTrue(self.form(form_data, form_files).is_valid(),
                        'Should be valid if sufficient data is given')
