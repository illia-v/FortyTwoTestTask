"""
There are functions which create model instances
They are used in test cases to make code DRY
"""
from datetime import date
from StringIO import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile

from .image import TEST_IMAGE
from .. import models


def person_info():
    return models.PersonInfo.objects.create(
        first_name='John', second_name='Fake',
        birth_date=date(year=1900, month=1, day=1),
        bio='my bio', email='john@fake.com', jabber='john@fake.com',
        skype='john_fake', other_contacts='nothing'
    )


def add_photo_to_person_info_instance(instance):
    instance.photo = InMemoryUploadedFile(
        StringIO(TEST_IMAGE),
        field_name='photo',
        name='mt_photo.jpg',
        content_type='image/jpg',
        size=len(TEST_IMAGE),
        charset='utf-8',
    )
    instance.save()
