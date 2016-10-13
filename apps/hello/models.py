from django.db import models


class PersonInfo(models.Model):
    """
    A model which contains information about a person
    """
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    bio = models.TextField()
    email = models.EmailField()
    jabber = models.EmailField()
    skype = models.CharField(max_length=20)
    other_contacts = models.TextField()

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.second_name)
