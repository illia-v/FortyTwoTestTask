import datetime
from StringIO import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from django.utils.timezone import now

from ..forms import HelloEditForm
from .image import TEST_IMAGE


class TestHelloEditForm(TestCase):
    def setUp(self):
        self.form = HelloEditForm
        self.sufficient_form_data = {
            'first_name': 'John', 'second_name': 'Fake',
            'birth_date': datetime.date(year=1900, month=1, day=1),
            'bio': 'my bio', 'email': 'john@fake.com',
            'jabber': 'john@fake.com', 'skype': 'john_fake',
            'other_contacts': 'nothing',
        }

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
        self.assertTrue(
            self.form(self.sufficient_form_data, form_files).is_valid(),
            'Should be valid if sufficient data is given'
        )

    def test_hello_edit_form_without_photo(self):
        """
        Ensures that `HelloEditForm` is valid if there is not only
        a photo
        """
        self.assertTrue(self.form(self.sufficient_form_data).is_valid(),
                        'Should be valid if there is not only a photo')

    def test_person_info_birth_date(self):
        """
        Ensures that `HelloEditForm` limits posible birth dates
        """
        future_date = now().date()+datetime.timedelta(days=1)
        self.sufficient_form_data.update({'birth_date': future_date})
        self.assertFalse(self.form(self.sufficient_form_data).is_valid(),
                         'Birth date should not be in the future')

        too_old_date = now().date().replace(year=now().year-200)
        self.sufficient_form_data.update({'birth_date': too_old_date})
        self.assertFalse(self.form(self.sufficient_form_data).is_valid(),
                         'Birth date should not be too old')
