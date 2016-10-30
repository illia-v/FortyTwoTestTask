import os.path
from StringIO import StringIO

from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from .validators import validate_birth_date
from fortytwo_test_task.settings.common import MEDIA_ROOT


class PersonInfo(models.Model):
    """
    A model that contains information about a person
    """
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    birth_date = models.DateField(validators=[validate_birth_date])
    bio = models.TextField()
    photo = models.ImageField(upload_to='photos', null=True)
    email = models.EmailField()
    jabber = models.EmailField()
    skype = models.CharField(max_length=20)
    other_contacts = models.TextField()

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.second_name)

    def save(self, *args, **kwargs):
        if self.photo and (self.photo.width or self.photo.height) > 200:
            photo = Image.open(self.photo)
            photo.thumbnail((200, 200))

            photo_output = StringIO()
            photo.save(photo_output, format='JPEG', quality=90)
            photo_output.seek(0)

            self.photo = InMemoryUploadedFile(
                photo_output, 'ImageField', '%s.jpg' % self.photo.name,
                'image/jpeg', photo_output.len, None)

        super(PersonInfo, self).save(*args, **kwargs)
