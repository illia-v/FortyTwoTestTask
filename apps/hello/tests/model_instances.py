"""
There are functions which create model instances
They are used in test cases to make code DRY
"""
from datetime import date

from .. import models


def person_info():
    return models.PersonInfo.objects.create(
        first_name='John', second_name='Fake',
        birth_date=date(year=1900, month=1, day=1),
        bio='my bio', email='john@fake.com', jabber='john@fake.com',
        skype='john_fake', other_contacts='nothing'
    )
