# -*- coding: utf-8 -*-
from StringIO import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase

from . import model_instances
from .image import TEST_IMAGE


class TestPersonInfo(TestCase):
    """
    A test case for a model `PersonInfo`
    """
    def setUp(self):
        self.person_info = model_instances.person_info()

    def test_init(self):
        """
        Ensures that the instance of the `PersonInfo` model can be
        created
        """
        self.assertIsNotNone(self.person_info.pk, 'Should have an instance')

    def test_person_info_unicode(self):
        """
        Ensures that the method `__unicode__` of the `PersonInfo` model
        returns a valid string
        """
        self.person_info.first_name = self.person_info.second_name = u'Їя'
        self.person_info.save()
        self.assertEqual(self.person_info.__unicode__(), u'Їя Їя',
                         'Method `__unicode__` of the `PersonInfo` model '
                         'should return a valid string')

    def test_person_info_scales_photo_to_200x200(self):
        """
        Ensures `PersonInfo` photo is scaled to 200x200
        """
        self.person_info = model_instances.person_info()
        self.person_info.photo = InMemoryUploadedFile(
            StringIO(TEST_IMAGE),
            field_name='photo',
            name='mt_photo.jpg',
            content_type='image/jpg',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )
        self.person_info.save()

        photo = self.person_info.photo

        self.assertLessEqual(photo.width and photo.height, 200,
                             'Photo should be scaled to 200x200, maintaining '
                             'aspect ratio, before saving')
